from pathlib import Path

import cv2 as cv
import numpy as np
from easyocr import Reader
from ultralytics import YOLO

from manga_colorizer.models.speech_bubble_segmenter import (
    get_speech_bubble_segmenter,
)


class PanelCleaner:
    """
    Removes text from manga panels
    """

    def __init__(self):
        self._bubble_segmenter: YOLO = get_speech_bubble_segmenter()
        self._text_detector = Reader(lang_list=["en"])

    def process(self, img_path: str | Path):
        img_path = str(img_path)

        original_image = cv.imread(img_path)

        segment_result = self._bubble_segmenter.predict(img_path)[0]
        text_result = self._text_detector.readtext(img_path)

        # Create speech bubble mask
        bubble_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
        if segment_result.masks is not None:
            for mask in segment_result.masks.data:
                mask_np = mask.cpu().numpy().astype(np.uint8)
                mask_np = cv.resize(
                    mask_np, (original_image.shape[1], original_image.shape[0])
                )
                bubble_mask = cv.bitwise_or(bubble_mask, mask_np)

        # Create text mask
        text_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
        for bbox, text, prob in text_result:
            # Convert bbox to integer coordinates
            (tl, tr, br, bl) = bbox
            tl = tuple(map(int, tl))
            br = tuple(map(int, br))

            # Draw filled rectangle on text mask
            cv.rectangle(text_mask, tl, br, 255, -1)

        composite_mask = cv.bitwise_and(bubble_mask, text_mask)

        masked_image = cv.bitwise_and(
            original_image, original_image, mask=composite_mask
        )

        return masked_image

    def display(self, img_path: str | Path):
        img_path = str(img_path)

        original_image = cv.imread(img_path)
        masked_image = self.process(img_path)

        # Create a combined image for side-by-side display
        h, w = original_image.shape[:2]
        combined_image = np.zeros((h, w * 2, 3), dtype=np.uint8)
        combined_image[:, :w] = original_image
        combined_image[:, w:] = masked_image

        # Add labels to the combined image
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(
            combined_image,
            "Original",
            (10, 30),
            font,
            1,
            (255, 255, 255),
            2,
            cv.LINE_AA,
        )
        cv.putText(
            combined_image,
            "Masked",
            (w + 10, 30),
            font,
            1,
            (255, 255, 255),
            2,
            cv.LINE_AA,
        )

        # Display the combined image
        cv.imshow("Original vs Masked", combined_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
