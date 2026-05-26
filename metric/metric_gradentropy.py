import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
# graduation_metric.py
#
# Calculates the histogram entropy of an image in C:\TEMP\QCImages.
# Histogram entropy measures the randomness or uniformity of the pixel intensity
# distribution. A higher value suggests a more even distribution of tones and,
# generally, better tonal graduation.

import cv2
import numpy as np

def calculate_histogram_entropy(image_path):
    """
    Calculates the histogram entropy of a grayscale image.

    Args:
        image_path (str): The full path to the input image file.

    Returns:
        float: The entropy value. A higher value indicates better tonal distribution.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Calculate the histogram of the grayscale image
    hist, _ = np.histogram(image.ravel(), 256, [0, 256])

    # Normalize the histogram to get probability distribution
    hist_norm = hist / hist.sum()

    # Calculate entropy; avoid log(0) by filtering zero probabilities
    probabilities = hist_norm[hist_norm > 0]
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return entropy

if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()
    file_name = os.path.basename(img_path)

    try:
        entropy_score = calculate_histogram_entropy(img_path)
        print(f"Image: {file_name}")
        print(f"  Histogram Entropy = {entropy_score:.2f}")
    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")
