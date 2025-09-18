import cv2
import numpy as np
from skimage import restoration
import os

def estimate_blur_with_richardson_lucy(image_path, num_iter=30, psf_size=11):
    """
    Estimates the blur in an image using Richardson-Lucy deconvolution.
    The metric is based on the difference between the original and deblurred image.
    A larger score indicates more blur.

    Parameters:
        image_path (str): The path to the image file.
        num_iter (int): The number of iterations for the algorithm.
        psf_size (int): The initial guess for the PSF size.

    Returns:
        float: A metric for blur, based on the difference between original and deblurred image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    image = image.astype(np.float32) / 255.0

    # Create a simple initial PSF (Point Spread Function) guess
    psf = np.ones((psf_size, psf_size)) / (psf_size ** 2)

    # Perform deconvolution using the correct parameter name
    deconvolved_image = restoration.richardson_lucy(image, psf, num_iter=num_iter)
    
    # Calculate a simple metric: the mean squared error between the original
    # and the deconvolved image.
    blur_metric = np.mean((image - deconvolved_image) ** 2)
    
    return blur_metric

# --- Main part of the script ---
if __name__ == "__main__":
    folder_name = "QCImages"
    file_name = "QCRef.jpg"
    
    image_path = os.path.join(folder_name, file_name)

    try:
        blur_metric = estimate_blur_with_richardson_lucy(image_path)
        print(f"Richardson-Lucy Blur Metric for {file_name}: {blur_metric:.6f}")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")