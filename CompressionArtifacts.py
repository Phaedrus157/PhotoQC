import sys
from PIL import Image
import numpy as np
from scipy.signal import convolve2d
from image_utils import get_qc_image_path

def analyze_compression_artifacts(image_path):
    """
    Analyzes an image for JPEG compression artifacts (blocking).
    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image and convert to grayscale for simplicity
        img = Image.open(image_path).convert('L') 
        img_array = np.array(img).astype(np.float32)
        
        print(f"✅ Successfully loaded image: {image_path}")
        print("\n--- Compression Artifact Analysis ---")

        # Define a kernel to detect 8x8 block artifacts
        # This kernel produces high values where there are sharp transitions
        # typical of block boundaries in compressed images.
        kernel_block = np.array([
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1,  8,  8,  8,  8,  8,  8,  8, -1],
            [-1,  8, -1, -1, -1, -1, -1,  8, -1],
            [-1,  8, -1,  8,  8,  8, -1,  8, -1],
            [-1,  8, -1,  8, -1,  8, -1,  8, -1],
            [-1,  8, -1,  8,  8,  8, -1,  8, -1],
            [-1,  8, -1, -1, -1, -1, -1,  8, -1],
            [-1,  8,  8,  8,  8,  8,  8,  8, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])

        # Apply the kernel using 2D convolution
        artifact_map = convolve2d(img_array, kernel_block, mode='valid')

        # Calculate a metric based on the mean squared values of the artifact map
        # A higher value indicates more pronounced blockiness
        artifact_score = np.mean(artifact_map**2)
        
        print(f"Artifact Score: {artifact_score:.2f}")

        # Interpret the score (these values are general guidelines)
        if artifact_score < 100:
            print("Conclusion: Minimal compression artifacts detected. High image quality.")
        elif artifact_score < 500:
            print("Conclusion: Moderate compression artifacts detected. Image quality may be impacted.")
        else:
            print("Conclusion: Significant compression artifacts detected. Image quality is likely low.")
            
        print("\nNote: This is a simplified metric. More advanced analysis may be needed.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_compression_artifacts(image_file)    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")