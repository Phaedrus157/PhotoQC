import cv2
import numpy as np

def calculate_brenner_sharpness(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Brenner metric calculation
    # Shift image by 2 pixels vertically and compute squared difference
    shifted = np.roll(image, -2, axis=0)
    diff = image[:-2, :] - shifted[:-2, :]
    brenner_metric = np.sum(diff ** 2)

    return brenner_metric

if __name__ == "__main__":
    img_path = "/workspaces/PhotoQC/ImageQC/_9093103.jpg"
    sharpness = calculate_brenner_sharpness(img_path)
    print(f"Brenner sharpness metric: {sharpness}")