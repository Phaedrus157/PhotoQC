import cv2
import numpy as np
import os
import sys

def calculate_laplacian_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return cv2.Laplacian(image, cv2.CV_64F).var()

def calculate_brenner_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    shifted = np.roll(image, -2, axis=0)
    diff = image[:-2, :] - shifted[:-2, :]
    return np.sum(diff ** 2)

def calculate_tenengrad_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    return np.sum(magnitude**2)

def calculate_gabor_variance(image_path, ksize=31, sigma=4.0, theta=0, lambd=10.0, gamma=0.5, psi=0):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_64F)
    filtered = cv2.filter2D(image, cv2.CV_64F, gabor_kernel)
    return np.var(filtered)

def get_metrics(image_path):
    return [
        calculate_laplacian_sharpness(image_path),
        calculate_brenner_sharpness(image_path),
        calculate_tenengrad_sharpness(image_path),
        calculate_gabor_variance(image_path)
    ]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py suite_sharpness_reference.py <reference_image> <test_image>")
        sys.exit(1)
    ref_path = sys.argv[1]
    comp_path = sys.argv[2]
    ref_filename = os.path.basename(ref_path)
    comp_filename = os.path.basename(comp_path)
    try:
        metrics_names = ["Laplacian Value", "Brenner Value", "Tenengrad Value", "Gabor Variance"]
        ref_metrics = get_metrics(ref_path)
        comp_metrics = get_metrics(comp_path)
        print(f"{'Metric':<20} {ref_filename:<20} {comp_filename:<20}")
        print("-" * 62)
        for name, ref, comp in zip(metrics_names, ref_metrics, comp_metrics):
            print(f"{name:<20} {ref:<20.4f} {comp:<20.4f}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")