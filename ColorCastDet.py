# color_cast_detector.py

import os
import cv2
import numpy as np

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
    image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")
    detect_color_cast(image_file)
