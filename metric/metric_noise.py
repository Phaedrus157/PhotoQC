import sys
import cv2
import numpy as np
from PIL import Image
from image_utils import get_qc_image_path

def analyze_noise(image_path: str):
    """
    Analyzes an image for overall noise as well as separate luminance and chrominance noise.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # --- Overall Noise Analysis using OpenCV (Laplacian Filter) ---
        print("\n--- Overall Noise Analysis ---")
        
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"File not found or unable to read: {image_path}")
            
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply the Laplacian filter
        laplacian_image = cv2.Laplacian(gray_image, cv2.CV_64F)
        
        # Calculate the variance as a metric for overall noise
        overall_noise_metric = np.var(laplacian_image)
        
        print(f"📈 Overall Noise Metric (Laplacian Variance): {overall_noise_metric:.2f}")

        # --- Advanced Noise Analysis (Luminance vs. Chrominance) ---
        print("\n--- Advanced Noise Analysis ---")

        # Load the image again using Pillow to convert to YCbCr
        pil_img = Image.open(image_path)
        ycbcr_img = pil_img.convert('YCbCr')
        ycbcr_array = np.array(ycbcr_img)

        # Split the channels
        y_channel = ycbcr_array[:,:,0]  # Luminance
        cb_channel = ycbcr_array[:,:,1] # Chrominance (Blue-difference)
        cr_channel = ycbcr_array[:,:,2] # Chrominance (Red-difference)
        
        # Simple function to calculate noise from a single channel's standard deviation
        def calculate_std_noise(channel):
            return np.std(channel)

        # Calculate noise for each channel based on standard deviation
        y_noise = calculate_std_noise(y_channel)
        cb_noise = calculate_std_noise(cb_channel)
        cr_noise = calculate_std_noise(cr_channel)
        
        # Combined chrominance noise score
        chroma_noise = (cb_noise + cr_noise) / 2
        
        print(f"📊 Luminance Noise (Y-channel): {y_noise:.2f}")
        print(f"🎨 Chrominance Noise (Cb/Cr-channels): {chroma_noise:.2f}")

        # Final Conclusion
        print("\n--- Analysis Conclusion ---")
        if y_noise > chroma_noise:
            print("Luminance noise is more dominant. The image appears grainy.")
        elif chroma_noise > y_noise:
            print("Chrominance noise is more dominant. The image has noticeable color blotchiness.")
        else:
            print("Luminance and chrominance noise levels are balanced.")
        
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_noise(image_file)    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")