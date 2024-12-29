from pathlib import Path

import cv2 as cv
import numpy as np

from manga_colorizer.processors.image_comparer import ImageComparer

color_path = Path("./manga-raw/color1/")
color_img_paths = [
    path
    for chapter_path in color_path.iterdir()
    if chapter_path.is_dir()
    if chapter_path.is_dir() and "1001" in chapter_path.name
    for path in chapter_path.iterdir()
]

ink_path = Path("./manga-raw/ink1/")
ink_img_paths = [
    path
    for chapter_path in ink_path.iterdir()
    if chapter_path.is_dir()
    if chapter_path.is_dir() and "1001" in chapter_path.name
    for path in chapter_path.iterdir()
]


def display(img_path, masked_path):
    """
    Helper for showing images side-by-side, normalized to the same size
    """
    img_path = str(img_path)
    masked_path = str(masked_path)

    original_image = cv.imread(img_path)
    masked_image = cv.imread(masked_path)

    # Determine the target size (smaller of the two images)
    h1, w1 = original_image.shape[:2]
    h2, w2 = masked_image.shape[:2]
    target_h = min(h1, h2)
    target_w = min(w1, w2)

    # Resize both images to the target size
    original_image = cv.resize(original_image, (target_w, target_h))
    masked_image = cv.resize(masked_image, (target_w, target_h))

    # Create a combined image for side-by-side display
    combined_image = np.zeros((target_h, target_w * 2, 3), dtype=np.uint8)
    combined_image[:, :target_w] = original_image
    combined_image[:, target_w:] = masked_image

    # Add labels to the combined image
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = min(
        1, target_h / 300
    )  # Adjust font size based on image height
    cv.putText(
        combined_image,
        "Ink",
        (10, 30),
        font,
        font_scale,
        (255, 255, 255),
        2,
        cv.LINE_AA,
    )
    cv.putText(
        combined_image,
        "Color",
        (target_w + 10, 30),
        font,
        font_scale,
        (255, 255, 255),
        2,
        cv.LINE_AA,
    )

    # Display the combined image
    cv.imshow("Original vs Masked", combined_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def test_display_most_similar():
    img_path = ink_img_paths[0]
    comparer = ImageComparer()
    most_similar_img_path = comparer.get_most_similar(img_path, color_img_paths)

    display(img_path, most_similar_img_path)


def test_display_best_pair():
    comparer = ImageComparer()
    pairs = comparer.pair(ink_img_paths, color_img_paths)
    for ink, color in pairs:
        display(ink, color)


if __name__ == "__main__":
    print("what")
    test_display_most_similar()
    print("the")
