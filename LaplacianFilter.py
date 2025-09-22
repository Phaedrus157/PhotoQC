import cv2
import os

def calculate_laplacian_sharpness(image_path):
    """
    Calculates image sharpness using the variance of the Laplacian.

    A higher variance value indicates a sharper image with more detail.
    A lower variance value indicates a blurrier image.

    Parameters:
        image_path (str): The full path to the image file.

    Returns:
        float: The variance of the Laplacian.
    """
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # If the image failed to load, return an error
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Apply the Laplacian filter and calculate the variance
    # cv2.CV_64F is used for high precision to avoid data loss
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()

    return laplacian_var

# --- Main part of the script ---
if __name__ == "__main__":
    # Define the image file name and its folder
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    
    # Construct the full image path
    image_path = os.path.join(folder_name, file_name)

    try:
        sharpness_score = calculate_laplacian_sharpness(image_path)
        print(f"The Laplacian sharpness score for {file_name} is: {sharpness_score:.2f}")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")