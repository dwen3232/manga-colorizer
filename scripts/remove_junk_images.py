import json
from pathlib import Path

import cv2
import matplotlib.pyplot as plt


def display_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title(f"Image: {image_path}")
    plt.tight_layout()


def on_key(event):
    if event.key == "d":
        delete_list.append(current_image)
        plt.close()
    elif event.key == "k":
        keep_list.append(current_image)
        plt.close()


def process_images(image_paths: list[str]):
    global current_image, delete_list, keep_list
    delete_list = []
    keep_list = []

    for image_path in image_paths:
        current_image = image_path
        display_image(image_path)

        fig = plt.gcf()
        fig.canvas.mpl_connect("key_press_event", on_key)

        plt.show()

    # Serialize the lists
    with open("delete_list.json", "w") as f:
        json.dump(delete_list, f)

    with open("keep_list.json", "w") as f:
        json.dump(keep_list, f)

    print(f"Deleted images: {len(delete_list)}")
    print(f"Kept images: {len(keep_list)}")


# Example usage
image_paths = [
    "path/to/image1.jpg",
    "path/to/image2.jpg",
    "path/to/image3.jpg",
    # Add more image paths here
]

process_images(image_paths)
