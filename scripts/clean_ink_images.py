import os
import sys
from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from sklearn.svm import SVC

A_MEAN_THRESH = 10
B_MEAN_THRESH = 10
A_STD_THRESH = 10
B_STD_THRESH = 10

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))


def compute_statistics(img_path: Path):
    img = cv2.imread(str(img_path))
    chan_l, chan_a, chan_b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))

    a_mean = chan_a.mean()
    a_abs_max = abs(chan_a).max()
    b_mean = chan_b.mean()
    b_abs_max = abs(chan_b).max()
    return [a_mean, a_abs_max, b_mean, b_abs_max]


def is_image_color(img_path: Path) -> bool:
    img = cv2.imread(str(img_path))
    chan_l, chan_a, chan_b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))

    stats = {}
    stats["a_mean"] = a_mean = np.mean(chan_a)  # type: ignore[arg-type]
    stats["a_std"] = a_std = np.std(chan_a)  # type: ignore[arg-type]
    stats["b_mean"] = b_mean = np.mean(chan_b)  # type: ignore[arg-type]
    stats["b_std"] = b_std = np.std(chan_b)  # type: ignore[arg-type]
    logger.debug(f"{img_path=} {stats}")

    if (
        abs(a_mean) < A_MEAN_THRESH
        and abs(b_mean) < B_MEAN_THRESH
        and a_std < A_STD_THRESH
        and b_std < B_STD_THRESH
    ):
        return True
    return False


if __name__ == "__main__":
    ink_path = Path("./manga-raw/ink1/manga_one-piece-chapter-1046/")
    img_paths = [path for path in ink_path.iterdir()]
    # filtered_img_paths = [
    #     path for path in img_paths if not is_image_color(path)
    # ]
    #
    # print(f"Found {len(img_paths)=}, {len(filtered_img_paths)=}")
    ink_features = np.array([compute_statistics(path) for path in img_paths])
    logger.debug(f"{ink_features.shape=}")

    svc = SVC()
    svc.fit(ink_features, np.ones((ink_features.shape[0],), dtype=np.int8))
    score = svc.score(ink_features, np.ones((ink_features.shape[0],), dtype=np.int8))
    logger.info(f"Scored {score=}")

