# dynamic_range_metrics.py
#
# This script calculates two metrics for assessing the dynamic range of
# images found in the 'QCImages' folder.
# 1. Luminance Standard Deviation: A higher value suggests a wider range of
#    brightness values, indicating better dynamic range.
# 2. Pixel Intensity Range: The difference between the brightest and darkest
#    pixels in the image.

import cv2
import numpy as np
import os
import glob

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

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # The V channel represents the value or luminance of the image
    luminance_channel = hsv[:, :, 2]
    
    # Calculate the standard deviation
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

    # Find the minimum and maximum pixel values
    min_val = np.min(image)
    max_val = np.max(image)
    
    # Calculate the range
    intensity_range = max_val - min_val
    return intensity_range

if __name__ == "__main__":
    # Define the directory where your images are located
    image_directory = "QCImages"
    
    # Get a list of all image files (jpg and png) in the specified directory
    image_files = glob.glob(os.path.join(image_directory, "*.jpg")) + glob.glob(os.path.join(image_directory, "*.png"))
    
    if not image_files:
        print(f"No image files found in the '{image_directory}' directory.")
    else:
        print(f"Found {len(image_files)} image(s) to analyze.")
        print("---")
        for img_path in image_files:
            file_name = os.path.basename(img_path)
            
            try:
                std_dev_score = calculate_luminance_std_dev(img_path)
                intensity_range = calculate_pixel_intensity_range(img_path)
                
                print(f"Image: {file_name}")
                print(f"  Luminance Standard Deviation = {std_dev_score:.2f}")
                print(f"  Pixel Intensity Range = {intensity_range}")
                print("---")
            except Exception as e:
                print(f"An error occurred while processing {file_name}: {e}")
