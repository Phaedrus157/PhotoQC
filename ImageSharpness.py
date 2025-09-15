import sys
import cv2
import numpy as np
from PIL import Image

def analyze_sharpness(image_path: str):
    """
    Analyzes an image for sharpness by calculating the variance of the
    Laplacian of the image.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"File not found or unable to read: {image_path}")
        
        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Image Sharpness Analysis ---")

        # Calculate the Laplacian of the image
        # The Laplacian highlights regions of rapid intensity change (i.e., edges)
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

        print(f"Sharpness Score (Laplacian Variance): {laplacian_var:.2f}")

        # Interpretation of the score
        # These thresholds are highly subjective and depend on the image content and resolution
        if laplacian_var < 50:
            print("Conclusion: The image is very soft and likely out of focus.")
        elif laplacian_var < 100:
            print("Conclusion: The image is soft but generally acceptable.")
        elif laplacian_var < 250:
            print("Conclusion: The image is reasonably sharp.")
        else:
            print("Conclusion: The image is very sharp and highly detailed.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Define the fixed image path
    image_file = "QCImages/QCRef.jpg"
    analyze_sharpness(image_file)