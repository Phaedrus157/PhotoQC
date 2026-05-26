import sys
from PIL import Image
import numpy as np
from image_utils import get_qc_image_path

def analyze_vignetting(image_path):
    """
    Analyzes an image for vignetting (light falloff) by comparing
    the average brightness of the center to the corners.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image and convert it to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img).astype(np.float32)

        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Vignetting Analysis ---")

        height, width = img_array.shape
        
        # Define the size of the center and corner regions (e.g., 20% of the image size)
        center_width = int(width * 0.2)
        center_height = int(height * 0.2)
        
        # Get the center region of the image
        center_region = img_array[
            height//2 - center_height//2 : height//2 + center_height//2,
            width//2 - center_width//2 : width//2 + center_width//2
        ]
        
        # Calculate the average brightness of the center
        center_brightness = np.mean(center_region)
        
        # Get the four corner regions
        corners = np.concatenate([
            img_array[:center_height, :center_width].flatten(),  # Top-left
            img_array[:center_height, -center_width:].flatten(), # Top-right
            img_array[-center_height:, :center_width].flatten(), # Bottom-left
            img_array[-center_height:, -center_width:].flatten() # Bottom-right
        ])
        
        # Calculate the average brightness of the corners
        corners_brightness = np.mean(corners)

        # Calculate the light falloff as a percentage
        if center_brightness == 0:
            vignetting_score = 0
        else:
            vignetting_score = ((center_brightness - corners_brightness) / center_brightness) * 100

        print(f"Center Brightness: {center_brightness:.2f}")
        print(f"Corners Brightness: {corners_brightness:.2f}")
        print(f"💡 Vignetting Score (Light Falloff): {vignetting_score:.2f}%")
        
        # Interpretation of the score
        if vignetting_score > 5:
            print("Conclusion: Significant vignetting detected. Corners are darker than the center.")
        elif vignetting_score > 1:
            print("Conclusion: Moderate vignetting detected. Corners are slightly darker than the center.")
        elif vignetting_score < -1:
            print("Conclusion: Reverse vignetting detected. Corners are brighter than the center.")
        else:
            print("Conclusion: Minimal to no vignetting detected.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_vignetting(image_file)    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")