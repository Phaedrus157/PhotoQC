"""
metric_laplacian_smoothed.py
Calculates image sharpness using variance of the Laplacian with
Gaussian pre-smoothing to reduce noise sensitivity.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2

def calculate_laplacian_sharpness(image_path, kernel_size=(5, 5), sigma=0):
    """
    Calculates image sharpness using the variance of the Laplacian.
    Applies Gaussian smoothing before computing the Laplacian to reduce noise.

    Parameters:
        image_path (str): Path to the image file.
        kernel_size (tuple): Size of the Gaussian kernel.
        sigma (float): Standard deviation for Gaussian kernel. 0 means auto-calculated.

    Returns:
        float: Variance of the Laplacian (sharpness score).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Could not load image.")

    # Apply Gaussian smoothing
    smoothed_image = cv2.GaussianBlur(image, kernel_size, sigma)

    # Compute Laplacian and calculate variance
    laplacian = cv2.Laplacian(smoothed_image, cv2.CV_64F)
    variance = laplacian.var()

    return variance

# --- Main part of the script ---
if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()

    try:
        sharpness_score = calculate_laplacian_sharpness(img_path)
        print(f"Laplacian sharpness score (with Gaussian smoothing) for {os.path.basename(img_path)}: {sharpness_score:.2f}")
    except Exception as e:
        print(f"Error: {e}")
