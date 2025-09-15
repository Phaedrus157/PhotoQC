import sys
import cv2
import numpy as np
from PIL import Image

def analyze_chromatic_aberration(image_path):
    """
    Analyzes an image for chromatic aberration (color fringing).
    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"File not found or unable to read: {image_path}")

        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Chromatic Aberration Analysis ---")

        # Convert the image to grayscale to find edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use Canny edge detection to find high-contrast edges
        edges = cv2.Canny(gray, 100, 200)

        # Split the image into its RGB channels
        b, g, r = cv2.split(img)

        # Shift the red and blue channels to align with the green channel
        # The green channel is typically the most stable reference
        # We find the shift that minimizes the difference
        best_r_shift = 0
        best_b_shift = 0
        min_r_diff = np.inf
        min_b_diff = np.inf
        
        # Search for the optimal shift within a small range
        for shift in range(-5, 6):
            # Roll (shift) the channel and calculate difference
            shifted_r = np.roll(r, shift, axis=1)
            diff_r = np.sum(np.abs(shifted_r - g))
            if diff_r < min_r_diff:
                min_r_diff = diff_r
                best_r_shift = shift

            shifted_b = np.roll(b, shift, axis=1)
            diff_b = np.sum(np.abs(shifted_b - g))
            if diff_b < min_b_diff:
                min_b_diff = diff_b
                best_b_shift = shift

        # A larger shift and difference indicates more chromatic aberration
        # Normalize the shift by the image width to get a relative score
        width = img.shape[1]
        score_r = abs(best_r_shift) / width * 100
        score_b = abs(best_b_shift) / width * 100
        
        # Combine the scores for a final result
        overall_score = (score_r + score_b) / 2

        print(f"Red Channel Shift (pixels): {best_r_shift}")
        print(f"Blue Channel Shift (pixels): {best_b_shift}")
        print(f"Overall Chromatic Aberration Score: {overall_score:.4f}%")
        
        # Interpretation of the score
        if overall_score < 0.01:
            print("Conclusion: Very low chromatic aberration. Excellent lens performance.")
        elif overall_score < 0.05:
            print("Conclusion: Minor chromatic aberration detected. Generally not visible.")
        else:
            print("Conclusion: Significant chromatic aberration detected. Fringing may be noticeable.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Define the fixed image path
    image_file = "QCImages/QCRef.jpg"
    analyze_chromatic_aberration(image_file)