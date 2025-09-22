import cv2
import numpy as np
import os
from image_utils import get_qc_image_path

def compute_local_variance(image_path, window_size=7):
    """
    Computes the local variance of an image using a sliding window.

    Parameters:
        image_path (str): Path to the input image.
        window_size (int): Size of the local window (must be odd).

    Returns:
        float: Mean local variance across the image.
    """
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Convert to float for precision
    image = image.astype(np.float32)

    # Compute local mean
    kernel = np.ones((window_size, window_size), np.float32) / (window_size ** 2)
    local_mean = cv2.filter2D(image, -1, kernel)

    # Compute local squared mean
    local_sq_mean = cv2.filter2D(image ** 2, -1, kernel)

    # Local variance = E[X^2] - (E[X])^2
    local_variance = local_sq_mean - local_mean ** 2

    # Return the mean of local variances as a global sharpness indicator
    return np.mean(local_variance)

# Example usage
if __name__ == "__main__":
    # Define the image path relative to the script's location
    # The folder name has been changed from 'QCImageRef' to 'QCImages'
    image_path = get_qc_image_path()
    try:
        score = compute_local_variance(image_path)
        print(f"Local Variance Score for QCRef2.jpg: {score:.2f}")
    except ValueError as e:
        print(e)