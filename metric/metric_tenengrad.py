"""
metric_tenengrad.py
Calculates image sharpness using the Tenengrad method (sum of squared
Sobel gradient magnitudes). Higher scores indicate sharper images.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np

def calculate_tenengrad_sharpness(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Compute Sobel gradients
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Tenengrad metric: sum of squared gradient magnitudes
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    tenengrad_metric = np.sum(magnitude**2)

    return tenengrad_metric

if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()

    try:
        sharpness = calculate_tenengrad_sharpness(img_path)
        print(f"Tenengrad sharpness metric for {os.path.basename(img_path)}: {sharpness:.4f}")
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
