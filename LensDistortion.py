import sys
import cv2
import numpy as np
from image_utils import get_qc_image_path

def analyze_lens_distortion(image_path):
    """
    Analyzes an image for lens distortion (barrel or pincushion).

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"File not found or unable to read: {image_path}")

        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Lens Distortion Analysis ---")

        # Use Canny edge detection to find edges
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        
        # Use Hough Lines Probabilistic Transform to find straight lines
        # This is more robust than the standard Hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        if lines is None:
            print("❌ No significant straight lines found to analyze distortion.")
            return

        # Initialize variables for distortion calculation
        distortion_scores = []
        center_x, center_y = img.shape[1] / 2, img.shape[0] / 2

        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate the midpoints of the line
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

            # Calculate the distance of the midpoint from the line connecting the endpoints
            # This is a proxy for how much the line segment is bowed
            
            # Equation of the line: ax + by + c = 0
            a = y2 - y1
            b = x1 - x2
            c = x2 * y1 - x1 * y2

            # Distance formula for a point (mid_x, mid_y) to a line (ax + by + c = 0)
            distance = abs(a * mid_x + b * mid_y + c) / np.sqrt(a**2 + b**2)
            
            # The sign of the distance can tell us the type of distortion
            # We can use the cross-product to determine the direction of the curve
            # If the line bows away from the center, it's barrel. Towards, it's pincushion.
            
            # Vector from center to midpoint of line
            vec_center_to_mid = (mid_x - center_x, mid_y - center_y)
            
            # Vector of the line itself
            vec_line = (x2 - x1, y2 - y1)
            
            # Find a perpendicular vector to the line
            vec_perp = (-vec_line[1], vec_line[0])

            # The sign of the dot product indicates the direction of curvature
            dot_product = vec_center_to_mid[0] * vec_perp[0] + vec_center_to_mid[1] * vec_perp[1]
            
            # A positive dot product implies pincushion, negative implies barrel
            distortion_type = 1 if dot_product > 0 else -1
            
            # Append the signed distance to the list
            distortion_scores.append(distance * distortion_type)
        
        if not distortion_scores:
            print("❌ No distortion metric could be calculated from the detected lines.")
            return

        # Calculate the average distortion score
        avg_distortion = np.mean(distortion_scores)
        
        # A simple normalization by image width
        normalized_score = abs(avg_distortion) / img.shape[1] * 100
        
        print(f"Average Distortion Score (normalized): {normalized_score:.4f}%")

        if avg_distortion > 0.1:
            print("Conclusion: Pincushion distortion detected. Straight lines appear to bow inward.")
        elif avg_distortion < -0.1:
            print("Conclusion: Barrel distortion detected. Straight lines appear to bow outward.")
        else:
            print("Conclusion: Minimal lens distortion detected. Lines are straight.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_lens_distortion(image_file)    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")