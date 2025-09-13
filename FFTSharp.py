import cv2
import numpy as np
import os

def calculate_fft_sharpness(image_path):
    """
    Calculates image sharpness using the Fast Fourier Transform (FFT).

    The metric is the ratio of high-frequency energy to total energy.
    A higher score indicates a sharper image.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        float: The FFT-based sharpness score.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Convert to float32 for FFT
    image_float = np.float32(image)

    # Perform the 2D FFT
    dft = cv2.dft(image_float, flags=cv2.DFT_COMPLEX_OUTPUT)
    
    # Shift the zero-frequency component to the center of the spectrum
    dft_shift = np.fft.fftshift(dft)

    # Calculate the magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))

    # Define the center and create masks for low and high frequencies
    rows, cols = image.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Create a low-frequency mask (e.g., a circle in the center)
    mask_size = 30
    low_freq_mask = np.zeros((rows, cols), dtype=np.uint8)
    cv2.circle(low_freq_mask, (center_col, center_row), mask_size, 255, -1)
    
    # Create a high-frequency mask (everything but the center)
    high_freq_mask = np.ones((rows, cols), dtype=np.uint8) * 255
    cv2.circle(high_freq_mask, (center_col, center_row), mask_size, 0, -1)

    # Extract magnitudes for low and high frequencies
    low_freq_energy = np.sum(magnitude_spectrum[low_freq_mask > 0])
    high_freq_energy = np.sum(magnitude_spectrum[high_freq_mask > 0])

    # Calculate the total energy
    total_energy = np.sum(magnitude_spectrum)

    # The metric is the ratio of high-frequency energy to total energy
    if total_energy == 0:
        return 0
    fft_sharpness_score = high_freq_energy / total_energy
    
    return fft_sharpness_score

# --- Main part of the script ---
if __name__ == "__main__":
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    image_path = os.path.join(folder_name, file_name)

    try:
        score = calculate_fft_sharpness(image_path)
        print(f"FFT Sharpness Score for {file_name}: {score:.6f}")
    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")