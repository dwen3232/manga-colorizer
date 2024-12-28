from pathlib import Path

import cv2 as cv
from matplotlib import pyplot as plt

if __name__ == "__main__":
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

    img = cv.imread(str(color_img_paths[0]), cv.IMREAD_GRAYSCALE)

    # Initiate ORB detector
    orb = cv.ORB_create()

    # find the keypoints with ORB
    kp = orb.detect(img, None)
    print(kp)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)
    plt.imshow(img2), plt.show()

#
# import cv2
# import numpy as np
# import os
#
# def match_images(color_dir, bw_dir):
#     color_images = [cv2.imread(os.path.join(color_dir, f)) for f in os.listdir(color_dir)]
#     bw_images = [cv2.imread(os.path.join(bw_dir, f), 0) for f in os.listdir(bw_dir)]
#     
#     # Initialize feature detector and matcher
#     orb = cv2.ORB_create()
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     
#     matches = []
#     for color_img in color_images:
#         gray_color = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
#         kp1, des1 = orb.detectAndCompute(gray_color, None)
#         
#         best_match = None
#         max_good_matches = 0
#         
#         for bw_img in bw_images:
#             kp2, des2 = orb.detectAndCompute(bw_img, None)
#             
#             # Match descriptors
#             matches = bf.match(des1, des2)
#             
#             # Sort them in order of distance
#             matches = sorted(matches, key=lambda x: x.distance)
#             
#             # Count good matches
#             good_matches = sum(1 for m in matches if m.distance < 50)
#             
#             if good_matches > max_good_matches:
#                 max_good_matches = good_matches
#                 best_match = bw_img
#         
#         matches.append((color_img, best_match))
#     
#     return matches
#
