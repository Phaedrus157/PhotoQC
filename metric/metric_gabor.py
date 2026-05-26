"""
metric_gabor.py
Calculates image sharpness/texture using Gabor filter variance.
Higher variance indicates more texture/detail in the image.

Usage: py metric_gabor.py <image_path>
"""

import cv2
import numpy as np
import os
import sys

def calculate_gabor_variance(image_path, ksize=31, sigma=4.0, theta=0, lambd=10.0, gamma=0.5, psi=0):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Create Gabor kernel
    gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_64F)
    # Apply Gabor filter
    filtered = cv2.filter2D(image, cv2.CV_64F, gabor_kernel)
    # Calculate variance of the filtered image
    variance = np.var(filtered)

    return variance

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py metric_gabor.py <image_path>")
        sys.exit(1)
    img_path = sys.argv[1]
    try:
        gabor_variance = calculate_gabor_variance(img_path)
        print(f"Gabor filter variance metric for {os.path.basename(img_path)}: {gabor_variance:.4f}")
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")