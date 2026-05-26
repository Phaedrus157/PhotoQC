import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from image_utils import get_qc_image_path

def analyze_tonal_distribution(image_path):
    """
    Analyzes the tonal distribution of an image, plotting its histogram
    and reporting on highlight and shadow clipping.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        print(f"✅ Successfully loaded image: {image_path}")

        # Convert the image to grayscale for luminance analysis
        gray_img = img.convert('L')
        img_array = np.array(gray_img)

        # Get total number of pixels in the image
        total_pixels = img_array.size
        if total_pixels == 0:
            print("❌ Error: The image has no pixels.")
            return

        # Calculate the histogram of the grayscale image
        # The range is 0-255 for 8-bit images
        histogram, bins = np.histogram(img_array, bins=256, range=[0, 255])

        # Find clipped pixels (pure black or pure white)
        shadow_pixels = histogram[0]  # Pixels with a value of 0 (pure black)
        highlight_pixels = histogram[255]  # Pixels with a value of 255 (pure white)

        # Calculate percentage of clipped pixels
        shadow_percent = (shadow_pixels / total_pixels) * 100
        highlight_percent = (highlight_pixels / total_pixels) * 100

        print("\n--- Tonal Analysis Summary ---")
        print(f"🌑 Clipped Shadows: {shadow_percent:.2f}% of pixels are pure black (value 0).")
        print(f"☀️ Clipped Highlights: {highlight_percent:.2f}% of pixels are pure white (value 255).")
        
        # Plot the histogram
        plt.figure(figsize=(10, 6))
        plt.plot(bins[:-1], histogram, color='black')
        plt.title('Luminance Histogram')
        plt.xlabel('Pixel Intensity (0=Black, 255=White)')
        plt.ylabel('Number of Pixels')
        plt.grid(True)

        # Highlight the clipping zones on the plot
        plt.axvspan(0, 5, color='red', alpha=0.3, label='Shadow Clipping Zone')
        plt.axvspan(250, 255, color='red', alpha=0.3, label='Highlight Clipping Zone')
        plt.legend()

        plt.show()
        
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_tonal_distribution(image_file)    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")