import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def extract_urls(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.text, "html.parser")
    urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc:  # Exclude fragment identifiers and invalid URLs
            urls.add(full_url)

    return list(urls)


def get_jpeg_urls(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.text, "html.parser")

    img_tags = soup.find_all("img")

    jpeg_urls = []
    for img in img_tags:
        src = img.get("src") or img.get("data-src")
        if src:
            # Make sure we have an absolute URL
            absolute_url = urljoin(url, src)
            # Check if the URL ends with .jpg or .jpeg (case-insensitive)
            if absolute_url.lower().endswith((".jpg", ".jpeg")):
                jpeg_urls.append(absolute_url)

    return jpeg_urls


if __name__ == "__main__":
    ink_url = "https://w29.onepiece-manga-online.net/manga/one-piece-chapter-1/"
    ink_base_url = "https://w29.onepiece-manga-online.net"
    all_urls = extract_urls(ink_base_url)
    chapter_urls = [url for url in all_urls if url.startswith(f"{ink_base_url}/manga")]

    for url in chapter_urls:
        print(url)
    print(len(chapter_urls))
    # jpegs = get_jpeg_urls(ink_url)
