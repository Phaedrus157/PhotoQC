# wavelet_sharpness.py
#
# This script calculates the sharpness of images in the 'QCImages' folder
# using a wavelet-based method. The method measures the energy of the
# high-frequency detail coefficients, with higher energy indicating sharper details.
#
# You may need to install the PyWavelets library: pip install PyWavelets

import cv2
import numpy as np
import pywt
import os
import glob

def calculate_wavelet_sharpness(image_path):
    """
    Calculates the sharpness of a single image based on the energy of high-frequency
    wavelet coefficients.

    Args:
        image_path (str): The full path to the input image file.

    Returns:
        float: The calculated sharpness score. A higher value indicates a sharper image.
    
    Raises:
        FileNotFoundError: If the specified image file does not exist.
        ImportError: If the pywt library is not installed.
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            # Check if the file exists at all to provide a more specific error
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")
            else:
                # If the file exists but cv2 can't read it, it might be corrupted or a non-image file
                print(f"Warning: Could not read image file {os.path.basename(image_path)}. Skipping.")
                return None

        # Convert image to float32 for wavelet transform
        image_float = np.float32(image)

        # Perform 2D discrete wavelet transform on the image
        # 'db1' is the Daubechies wavelet of order 1.
        coeffs = pywt.dwt2(image_float, 'db1')
        cA, (cH, cV, cD) = coeffs

        # Calculate the energy of the high-frequency components
        sharpness_score = np.sum(np.square(cH)) + np.sum(np.square(cV)) + np.sum(np.square(cD))

        return sharpness_score

    except ImportError:
        print("The 'pywt' library is not installed. Please install it with: pip install PyWavelets")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing {os.path.basename(image_path)}: {e}")
        return None

if __name__ == "__main__":
    # Define the directory where your images are located
    image_directory = "QCImages"
    
    # Get a list of all image files (jpg and png) in the specified directory
    image_files = glob.glob(os.path.join(image_directory, "*.jpg")) + glob.glob(os.path.join(image_directory, "*.png"))
    
    if not image_files:
        print(f"No image files found in the '{image_directory}' directory.")
    else:
        print(f"Found {len(image_files)} image(s) to analyze.")
        print("---")
        for img_path in image_files:
            file_name = os.path.basename(img_path)
            sharpness_score = calculate_wavelet_sharpness(img_path)
            if sharpness_score is not None:
                print(f"Image: {file_name}")
                print(f"  Wavelet Sharpness Score = {sharpness_score:.2f}")
                print("---")
