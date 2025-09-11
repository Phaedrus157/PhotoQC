import cv2
import numpy as np

def calculate_tenengrad_sharpness(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Compute Sobel gradients
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Tenengrad metric: sum of squared gradient magnitudes
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    tenengrad_metric = np.sum(magnitude**2)

    return tenengrad_metric

if __name__ == "__main__":
    img_path = "/workspaces/PhotoQC/ImageQC/_9093103.jpg"
    sharpness = calculate_tenengrad_sharpness(img_path)
    print(f"Tenengrad sharpness metric: {sharpness}")