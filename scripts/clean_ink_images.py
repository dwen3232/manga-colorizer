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


if __name__ == "__main__":
    ink_path = Path("./manga-raw/ink1/")
    color_path = Path("./manga-raw/color1/")

    ink_img_paths = [
        path
        for chapter_path in ink_path.iterdir()
        if chapter_path.is_dir() and "1001" in chapter_path.name
        for path in chapter_path.iterdir()
    ]
    color_img_paths = [
        path
        for chapter_path in color_path.iterdir()
        if chapter_path.is_dir() and "1001" in chapter_path.name
        for path in chapter_path.iterdir()
    ]
    logger.debug(f"Found {len(ink_img_paths)=} images")
    logger.debug(f"Found {len(color_img_paths)=} images")

    ink_features = np.array(
        [compute_statistics(path) for path in ink_img_paths]
    )
    color_features = np.array(
        [compute_statistics(path) for path in color_img_paths]
    )

    logger.debug(f"{ink_features.shape=}")
    logger.debug(f"{color_features.shape=}")

    features = np.concatenate([ink_features, color_features], axis=0)
    logger.debug(f"{features.shape=}")

    labels = np.concatenate(
        [
            np.zeros(ink_features.shape[0], dtype=np.bool),
            np.ones(color_features.shape[0], dtype=np.bool),
        ],
    )

    svc = SVC()
    svc.fit(features, labels)

    score = svc.score(
        ink_features, np.ones((ink_features.shape[0],), dtype=np.int8)
    )
    logger.info(f"Scored {score=}")

    predictions = svc.predict(ink_features)

    print(np.array(ink_img_paths)[predictions])
