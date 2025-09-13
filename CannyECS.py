import cv2
import os

def count_canny_edges(image_path, threshold1=100, threshold2=200):
    """
    Counts the number of pixels identified as edges by the Canny algorithm.

    A higher count suggests a more complex image with more edges.

    Parameters:
        image_path (str): The path to the image file.
        threshold1 (int): The first threshold for the Canny edge detector.
        threshold2 (int): The second threshold for the Canny edge detector.

    Returns:
        int: The number of detected edge pixels.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Apply the Canny edge detector
    edges = cv2.Canny(image, threshold1, threshold2)

    # Count the number of non-zero (edge) pixels
    edge_count = cv2.countNonZero(edges)

    return edge_count

# --- Main part of the script ---
if __name__ == "__main__":
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    
    image_path = os.path.join(folder_name, file_name)

    try:
        edge_count_score = count_canny_edges(image_path)
        print(f"Canny Edge Count for {file_name}: {edge_count_score}")
    except (FileNotFoundError, ValueError) as e:
        print(e)