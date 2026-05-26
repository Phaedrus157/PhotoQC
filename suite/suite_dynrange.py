"""
suite_dynrange.py
Dynamic range analysis suite combining luminance standard deviation
and pixel intensity range metrics.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np


def calculate_luminance_std_dev(image_path):
    """
    Calculates the standard deviation of the luminance channel (V in HSV)
    as a simple proxy for dynamic range. A higher standard deviation suggests
    a wider range of brightness values.

    Args:
        image_path (str): The path to the image file.

    Returns:
        float: The standard deviation of the luminance channel.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    luminance_channel = hsv[:, :, 2]
    std_dev = np.std(luminance_channel)
    return std_dev


def calculate_pixel_intensity_range(image_path):
    """
    Calculates the range of pixel intensities (max - min) in a grayscale image.
    This provides a basic measure of the image's dynamic range.

    Args:
        image_path (str): The path to the image file.

    Returns:
        int: The difference between the maximum and minimum pixel intensity.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    min_val = np.min(image)
    max_val = np.max(image)
    intensity_range = max_val - min_val
    return intensity_range


if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()
    file_name = os.path.basename(img_path)

    try:
        std_dev_score = calculate_luminance_std_dev(img_path)
        intensity_range = calculate_pixel_intensity_range(img_path)

        print(f"Image: {file_name}")
        print(f"  Luminance Standard Deviation = {std_dev_score:.2f}")
        print(f"  Pixel Intensity Range        = {intensity_range}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
