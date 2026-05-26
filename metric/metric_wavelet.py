import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
# wavelet_sharpness.py
#
# Calculates image sharpness using a wavelet-based method. Measures the energy
# of the high-frequency detail coefficients; higher energy indicates sharper details.
#
# You may need to install the PyWavelets library: pip install PyWavelets

import cv2
import numpy as np
import pywt

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
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")
            else:
                print(f"Warning: Could not read image file {os.path.basename(image_path)}. Skipping.")
                return None

        # Convert image to float32 for wavelet transform
        image_float = np.float32(image)

        # Perform 2D discrete wavelet transform ('db1' = Daubechies order 1)
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
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()
    file_name = os.path.basename(img_path)

    sharpness_score = calculate_wavelet_sharpness(img_path)
    if sharpness_score is not None:
        print(f"Image: {file_name}")
        print(f"  Wavelet Sharpness Score = {sharpness_score:.2f}")
