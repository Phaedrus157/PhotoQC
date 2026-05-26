import cv2
import numpy as np
from image_utils import get_qc_image_path

def analyze_chromatic_aberration(image_path):
    """
    Analyzes chromatic aberration (color fringing) in an image by measuring misalignment
    between color channels, particularly red and blue relative to green.

    A higher score indicates more chromatic aberration, which may result in visible color fringing
    around edges — often caused by lens imperfections.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        float: Overall chromatic aberration score as a percentage of image width.
    """
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"File not found or unable to read: {image_path}")

        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Chromatic Aberration Analysis ---")

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect edges using Canny to focus on high-contrast areas
        cv2.Canny(gray, 100, 200)

        # Split image into Blue, Green, Red channels
        b, g, r = cv2.split(img)

        # Initialize variables to track best alignment shifts
        best_r_shift = 0
        best_b_shift = 0
        min_r_diff = np.inf
        min_b_diff = np.inf

        # Search for optimal horizontal shift (-5 to +5 pixels)
        for shift in range(-5, 6):
            # Shift red channel and compare to green
            shifted_r = np.roll(r, shift, axis=1)
            diff_r = np.sum(np.abs(shifted_r - g))
            if diff_r < min_r_diff:
                min_r_diff = diff_r
                best_r_shift = shift

            # Shift blue channel and compare to green
            shifted_b = np.roll(b, shift, axis=1)
            diff_b = np.sum(np.abs(shifted_b - g))
            if diff_b < min_b_diff:
                min_b_diff = diff_b
                best_b_shift = shift

        # Normalize shifts by image width to get percentage score
        width = img.shape[1]
        score_r = abs(best_r_shift) / width * 100
        score_b = abs(best_b_shift) / width * 100
        overall_score = (score_r + score_b) / 2

        # --- Output Section ---
        print(f"🔴 Red Channel Shift (pixels): {best_r_shift}")
        print(f"🔵 Blue Channel Shift (pixels): {best_b_shift}")
        print(f"📊 Overall Chromatic Aberration Score: {overall_score:.4f}%")

        # --- Interpretation ---
        print("🔍 Interpretation:")
        if overall_score < 0.01:
            print(" - Very low chromatic aberration. Excellent lens performance.")
        elif overall_score < 0.05:
            print(" - Minor chromatic aberration detected. Generally not visible.")
        else:
            print(" - Significant chromatic aberration detected. Fringing may be noticeable.")

        return overall_score

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    try:
        image_file = get_qc_image_path()
        analyze_chromatic_aberration(image_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")