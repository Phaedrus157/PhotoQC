import cv2
import os

def count_canny_edges(image_path, threshold1=100, threshold2=200):
    """
    Calculates the number of edge pixels in an image using the Canny edge detection algorithm.

    A higher edge count generally indicates a sharper or more detailed image.
    This metric can help assess image complexity and sharpness.

    Parameters:
        image_path (str): Path to the image file.
        threshold1 (int): Lower threshold for edge detection.
        threshold2 (int): Upper threshold for edge detection.

    Returns:
        int: Number of pixels detected as edges.
    """
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Error: The image file was not found at {image_path}")

    # Load the image in grayscale mode
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("❌ Error: Could not load the image. Check file integrity.")

    # Apply Canny edge detection
    edges = cv2.Canny(image, threshold1, threshold2)

    # Count non-zero pixels (i.e., detected edges)
    edge_count = cv2.countNonZero(edges)

    return edge_count

# --- Main Execution Block ---
if __name__ == "__main__":
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    image_path = os.path.join(folder_name, file_name)

    try:
        edge_count_score = count_canny_edges(image_path)

        # Output section: print score and interpretation
        print(f"🧮 Canny Edge Count for {file_name}: {edge_count_score}")
        print("🔍 Interpretation:")
        print(" - Higher edge count = more detail or sharpness")
        print(" - Lower edge count = smoother or blurrier image")
        print(" - Use this metric to compare sharpness across images")

    except (FileNotFoundError, ValueError) as e:
        print(e)
