from pathlib import Path

import cv2 as cv
import easyocr
from loguru import logger

from manga_colorizer.models.speech_bubble_segmenter import (
    get_speech_bubble_segmenter,
)

seg_model = get_speech_bubble_segmenter()
reader = easyocr.Reader(["en"])


def clean_panels(path):
    result = seg_model.predict(path)[0]


def main():
    print("what")
    ink_path = Path("./manga-raw/ink1/")
    color_path = Path("./manga-raw/color1/")

    ink_img_paths = [
        path
        for chapter_path in ink_path.iterdir()
        if chapter_path.is_dir()
        if chapter_path.is_dir() and "1001" in chapter_path.name
        for path in chapter_path.iterdir()
    ]
    color_img_paths = [
        path
        for chapter_path in color_path.iterdir()
        if chapter_path.is_dir()
        if chapter_path.is_dir() and "1001" in chapter_path.name
        for path in chapter_path.iterdir()
    ]

    for path in ink_img_paths:
        image = cv.imread(str(path))
        height, width, channels = image.shape
        print(path)
        print(image.shape, height / width)

    for path in color_img_paths:
        image = cv.imread(str(path))
        height, width, channels = image.shape
        print(path)
        print(image.shape, height / width)

    # results = seg_model.predict(color_img_paths, stream=True)
    #
    # for result in results:
    #     print(type(result))
    #     result.show()

    seg_model = get_speech_bubble_segmenter()
    logger.info("Segmenting image")
    results = seg_model.predict(ink_img_paths[0])[0]

    reader_result = reader.readtext(str(ink_img_paths[0]))
    print(reader_result)
    results.show()


if __name__ == "__main__":
    print("what")
    main()
