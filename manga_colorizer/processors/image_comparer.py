from collections.abc import Sequence
from pathlib import Path

from loguru import logger
from PIL import Image
from torch import Tensor

from manga_colorizer.models.clip_encoder import get_clip_encoder


class ImageComparer:
    def __init__(self):
        self._clip = get_clip_encoder()

    def _encode(self, path: str | Path) -> Tensor:
        path = str(path)
        return self._clip.encode(Image.open(path))  # type: ignore[]

    def compare(self, img: str | Path, target_imgs: Sequence[str | Path]):
        # Initialize feature detector and matcher
        img_emb = self._encode(img)
        target_embs = [self._encode(target_img) for target_img in target_imgs]

        target_img_to_similarity = {
            target_img: self._clip.similarity(img_emb, target_emb)
            for target_img, target_emb in zip(target_imgs, target_embs)
        }
        logger.info(f"Computed the similaries {target_img_to_similarity}")
        print(target_img_to_similarity)

        return target_img_to_similarity

    def get_most_similar(
        self, img: str | Path, target_imgs: Sequence[str | Path]
    ):
        target_img_to_similarity = self.compare(img, target_imgs)
        min_target_img = max(
            target_img_to_similarity, key=target_img_to_similarity.get
        )

        return min_target_img

    def get_least_similar(
        self, img: str | Path, target_imgs: Sequence[str | Path]
    ):
        target_img_to_similarity = self.compare(img, target_imgs)
        min_target_img = min(
            target_img_to_similarity, key=target_img_to_similarity.get
        )

        return min_target_img

    def pair(
        self, src_imgs: Sequence[str | Path], target_imgs: Sequence[str | Path]
    ):
        similarity_stats = {
            (src_img, target_img): value
            for src_img in src_imgs
            for target_img, value in self.compare(src_img, target_imgs).items()
        }

        seen_srcs = set()
        seen_targets = set()
        pairs = []

        while similarity_stats:
            src, target = max(similarity_stats, key=similarity_stats.get)
            if src not in seen_srcs and target not in seen_targets:
                pairs.append((src, target))
                seen_srcs.add(src)
                seen_targets.add(target)
            similarity_stats.pop((src, target))
        return pairs
