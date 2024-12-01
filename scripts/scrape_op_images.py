import argparse
import asyncio
import json
import os
import re
import resource
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import aiofiles
import httpx
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

semaphore = asyncio.Semaphore(20)

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))


def increase_file_descriptor_limit(new_limit):
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    logger.info(f"File descriptor limit {soft=}, {hard=}")
    resource.setrlimit(resource.RLIMIT_NOFILE, (new_limit, hard))


increase_file_descriptor_limit(4096)

parser = argparse.ArgumentParser(
    description="Process a base URL and a pattern to match URL tails."
)

parser.add_argument(
    "base_url", help="The base URL path (e.g., 'https://base.com/')"
)
parser.add_argument(
    "--download_dir",
    help="Where to download images and metadata",
    default=Path("./downloads/default/"),
)
parser.add_argument(
    "--pattern",
    help="A pattern to match URLs (e.g., '^https://base.com/something$')",
    default=".*",
)
parser.add_argument(
    "--img_pattern",
    help="A pattern to match img sources by",
    default=".*(.webp|.jpeg|.jpg)$",
)
args = parser.parse_args()

logger.info(f"{args=}")


async def extract_urls(url: str, client: httpx.AsyncClient) -> list[str]:
    logger.debug(f"Getting {url=}...")
    response = await client.get(url)
    response.raise_for_status()
    logger.debug(f"Getting {url=} was successful!")

    soup = BeautifulSoup(response.text, "html.parser")
    urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc:
            urls.add(full_url)

    return list(urls)


async def get_image_urls(url: str, pattern: str, client: httpx.AsyncClient):
    logger.debug(f"Getting jpegs at {url=}...")
    response = await client.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    image_urls: list[str] = []
    for img in img_tags:
        src = img.get("src") or img.get("data-src")
        if src and re.match(pattern, src):
            image_urls.append(src)

    if image_urls:
        logger.debug(f"In {url=}, found {len(image_urls)=}!")
    else:
        logger.warning(f"In {url=}, found {len(image_urls)=}!")

    return url, image_urls


@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=4, max=120),
)
async def download_file(
    url: str,
    save_path: Path,
    client: httpx.AsyncClient,
):
    temp_path = Path(str(save_path) + ".tmp")
    os.makedirs(temp_path.parent, exist_ok=True)
    try:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            logger.debug(f"Writing to {temp_path=}")
            async with aiofiles.open(temp_path, "wb") as file:
                async for chunk in response.aiter_bytes():
                    await file.write(chunk)
        logger.debug(f"Downloaded: {url} -> {temp_path}")

        os.replace(temp_path, save_path)
        logger.debug(f"Moved {temp_path=} to {save_path=}")
    except Exception as e:
        logger.warning(f"Error downloading {url=}")
        os.remove(temp_path)
        raise e


async def download_image_group(
    image_urls: list[str],
    dir_name: str,
    client: httpx.AsyncClient,
    base_path=Path("./downloads/default/"),
):
    dir_name = urlparse(dir_name).path.strip("/").replace("/", "_")
    dir_path = base_path / dir_name
    download_tasks = []
    for image_url in image_urls:
        file_name = os.path.basename(urlparse(image_url).path)
        save_path = dir_path / file_name
        if not save_path.exists():
            logger.debug(f"{save_path=} doesn't exist!")

            download_tasks.append(download_file(image_url, save_path, client))

    async with semaphore:
        await asyncio.gather(*download_tasks)


async def write_metadata(
    data,
    file_path=Path("./downloads/default/metadata"),
):
    logger.debug("Writing metadata...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    async with aiofiles.open(file_path, "w") as f:
        await f.write(json.dumps(data, indent=2))
    logger.debug("Wrote metadata successfully")


async def main():
    """
    Read base_url -> Read list of chapter urls -> download all jpegs
    """
    base_url = args.base_url
    download_dir = Path(args.download_dir)
    pattern = args.pattern
    img_pattern = args.img_pattern

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(None),
        limits=httpx.Limits(
            max_connections=20,
        ),
    ) as client:
        all_urls = await extract_urls(base_url, client)
        matched_urls = (
            [url for url in all_urls if re.match(pattern, url)]
            if pattern
            else all_urls
        )
        errors = []
        tasks = []

        # Try to read img urls and download
        image_url_groups = {}

        for image_urls_task in asyncio.as_completed(
            get_image_urls(url, img_pattern, client) for url in matched_urls
        ):
            try:
                url, image_urls = await image_urls_task
                image_url_groups[url] = image_urls
                task = asyncio.create_task(
                    download_image_group(
                        image_urls, url, client, base_path=download_dir
                    )
                )
                tasks.append(task)
            except Exception as e:
                errors.append(e)

        # Try to write metadata
        if image_url_groups:
            logger.info(f"Found {len(image_url_groups)} groups")
            count_empty_groups = sum(
                (len(imgs) == 0) for imgs in image_url_groups.values()
            )
            logger.info(f"Found {count_empty_groups=} groups with no imgs")
            try:
                await write_metadata(
                    image_url_groups, file_path=download_dir / "metadata"
                )
            except Exception as e:
                errors.append(e)

        await asyncio.gather(*tasks)

        if errors:
            raise ExceptionGroup(f"Encountered {len(errors)=} errors", errors)


if __name__ == "__main__":
    asyncio.run(main())
