import cv2
import numpy as np
import os

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
    # The gradients show the rate of change of pixel intensity.
    grad_x = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)

    # Calculate the gradient magnitude (total edge strength at each pixel)
    # This is the Euclidean norm of the gradient vector at each pixel
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # Calculate the average of the gradient magnitudes
    average_gradient = np.mean(grad_magnitude)

    # Normalize the score by dividing by the maximum possible value (255 * sqrt(2))
    # This scales the score to a range of 0 to 1, making it easier to compare
    # images of different bit depths.
    normalized_average_gradient = average_gradient / (255 * np.sqrt(2))

    return normalized_average_gradient

# --- Main part of the script ---
if __name__ == "__main__":
    # Define the image file name and its folder
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    
    # Construct the full image path
    image_path = os.path.join(folder_name, file_name)

    try:
        score = calculate_normalized_average_gradient(image_path)
        print(f"Normalized Average Gradient for {file_name}: {score:.6f}")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")