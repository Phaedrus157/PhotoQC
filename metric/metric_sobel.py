import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np

def calculate_sobel_edge_intensity(image_path):
    """
    Calculates the total edge intensity using the Sobel operator.

    A higher value indicates a sharper image with stronger edges.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        float: The sum of the magnitudes of all detected edges.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Apply Sobel filters to find horizontal and vertical edges
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the magnitude of the gradient
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

    # Return the sum of all gradient magnitudes
    return np.sum(gradient_magnitude)

# --- Main part of the script ---
if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()

    try:
        intensity_score = calculate_sobel_edge_intensity(img_path)
        print(f"Sobel Edge Intensity Score for {os.path.basename(img_path)}: {intensity_score:.2f}")
    except (FileNotFoundError, ValueError) as e:
        print(e)
