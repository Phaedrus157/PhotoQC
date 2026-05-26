import cv2
import numpy as np
import os

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
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    
    image_path = os.path.join(folder_name, file_name)

    try:
        intensity_score = calculate_sobel_edge_intensity(image_path)
        print(f"Sobel Edge Intensity Score for {file_name}: {intensity_score:.2f}")
    except (FileNotFoundError, ValueError) as e:
        print(e)