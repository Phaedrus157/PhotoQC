"""
gaussian_smooth.py
Applies Gaussian smoothing to a grayscale image and saves the result.

Usage: py gaussian_smooth.py <input_image> <output_image>
"""

import cv2
import os
import sys

def apply_gaussian_smoothing(image_path, output_path, kernel_size=(3, 3), sigma=0):
    """
    Applies Gaussian smoothing to a grayscale image and saves the result.

    Parameters:
        image_path (str): Path to the input image.
        output_path (str): Path to save the smoothed image.
        kernel_size (tuple): Size of the Gaussian kernel.
        sigma (float): Standard deviation for Gaussian kernel.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Could not load image.")

    smoothed_image = cv2.GaussianBlur(image, kernel_size, sigma)
    cv2.imwrite(output_path, smoothed_image)

# --- Main part of the script ---
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py gaussian_smooth.py <input_image> <output_image>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    try:
        apply_gaussian_smoothing(input_path, output_path)
        print(f"Smoothed image saved to: {output_path}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")