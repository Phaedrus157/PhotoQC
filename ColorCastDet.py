# color_cast_detector.py

import os
import cv2
import numpy as np
from image_utils import get_qc_image_path

def detect_color_cast(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return None

    mean_colors = np.mean(image, axis=(0, 1))
    gray_level = np.mean(mean_colors)
    deviation = mean_colors - gray_level
    cast_strength = np.linalg.norm(deviation)

    print(f"🎨 Mean RGB: {mean_colors}")
    print(f"⚖️ Color Cast Strength: {cast_strength:.2f}")
    return cast_strength

if __name__ == "__main__":
    try:
        image_file = get_qc_image_path()
        detect_color_cast(image_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")