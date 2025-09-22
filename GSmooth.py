import cv2
import os
from image_utils import get_qc_image_path

def apply_gaussian_smoothing(image_path, output_path, kernel_size=(3, 3), sigma=0):
    """
    Applies Gaussian smoothing to a grayscale image and saves the result.

    Parameters:
        image_path (str): Path to the input image.
        output_path (str): Path to save the smoothed image.
        kernel_size (tuple): Size of the Gaussian kernel.
        sigma (float): Standard deviation for Gaussian kernel.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Could not load image.")

    smoothed_image = cv2.GaussianBlur(image, kernel_size, sigma)
    cv2.imwrite(output_path, smoothed_image)

# --- Main part of the script ---
if __name__ == "__main__":
    try:
        folder_name = "QCImages"
        image_path = get_qc_image_path()
        image_path = os.path.join(folder_name, file_name)
        output_file_name = "QCRef_smoothed.jpg"
        output_path = os.path.join(folder_name, output_file_name)

        apply_gaussian_smoothing(image_path, output_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")