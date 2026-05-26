import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np

def calculate_normalized_average_gradient(image_path):
    """
    Calculates the normalized average gradient of an image.

    This metric is a measure of overall edge strength. A higher score
    suggests a sharper image with more pronounced edges.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        float: The normalized average gradient score.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Convert to float for accurate gradient calculation
    image = image.astype(np.float32)

    # Calculate horizontal and vertical gradients using the Sobel operator
    grad_x = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)

    # Calculate the gradient magnitude (total edge strength at each pixel)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # Normalize by maximum possible value to scale 0-1
    average_gradient = np.mean(grad_magnitude)
    normalized_average_gradient = average_gradient / (255 * np.sqrt(2))

    return normalized_average_gradient

# --- Main part of the script ---
if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()

    try:
        score = calculate_normalized_average_gradient(img_path)
        print(f"Normalized Average Gradient for {os.path.basename(img_path)}: {score:.6f}")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
