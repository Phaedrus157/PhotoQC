# graduation_metric.py
#
# This script calculates the histogram entropy of images in the 'QCImages' folder.
# Histogram entropy measures the randomness or uniformity of the pixel intensity
# distribution. A higher value suggests a more even distribution of tones and,
# generally, better tonal graduation.

import cv2
import numpy as np
import os
import glob

def calculate_histogram_entropy(image_path):
    """
    Calculates the histogram entropy of a grayscale image.

    Args:
        image_path (str): The full path to the input image file.

    Returns:
        float: The entropy value. A higher value indicates better tonal distribution.
    
    Raises:
        FileNotFoundError: If the image file is not found.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Calculate the histogram of the grayscale image
    hist, _ = np.histogram(image.ravel(), 256, [0, 256])

    # Normalize the histogram to get probability distribution
    hist_norm = hist / hist.sum()

    # Calculate entropy using the formula: $H = - \sum_{i} p_i \log_2(p_i)$
    # Avoid log(0) by filtering out zero probabilities.
    probabilities = hist_norm[hist_norm > 0]
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return entropy

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
                entropy_score = calculate_histogram_entropy(img_path)
                
                print(f"Image: {file_name}")
                print(f"  Histogram Entropy = {entropy_score:.2f}")
                print("---")
            except Exception as e:
                print(f"An error occurred while processing {file_name}: {e}")
