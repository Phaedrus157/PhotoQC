import cv2
import numpy as np
import os

def calculate_brenner_sharpness(image_path):
    """
    Calculates image sharpness using the Brenner gradient method.
    This metric estimates sharpness based on vertical intensity changes.
    A higher score indicates a sharper image with more edge detail.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        float: Brenner sharpness score.
    """
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Shift image by 2 pixels vertically and compute squared difference
    shifted = np.roll(image, -2, axis=0)
    diff = image[:-2, :] - shifted[:-2, :]
    brenner_metric = np.sum(diff ** 2)

    return brenner_metric

# --- Main part of the script ---
if __name__ == "__main__":
    img_path = "/workspaces/PhotoQC/ImageQC/_9093103.jpg"

    try:
        sharpness = calculate_brenner_sharpness(img_path)
        print(f"📏 Brenner Sharpness Metric for {os.path.basename(img_path)}: {sharpness:.2f}")

        # Interpretation of the result
        print("📘 Interpretation:")
        print("- Higher values indicate more edge contrast and sharper images.")
        print("- Lower values suggest reduced detail or blur.")
        print("- This metric is relative; compare across images for best results.")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
