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
    try:
        folder = "/workspaces/PhotoQC/ImageQC"
        ref_filename = "QCRef.jpg"
        ref_path = os.path.join(folder, ref_filename)

        all_files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png")) and f != ref_filename]

        if len(all_files) == 0:
            print("No comparison image found in ImageQC folder.")
            sys.exit(1)
        elif len(all_files) > 1:
            print("Multiple comparison images found. Please keep only one alongside QCRef.jpg.")
            for f in all_files:
                print(f" - {f}")
            sys.exit(1)

        comp_filename = all_files[0]
        comp_path = os.path.join(folder, comp_filename)

        metrics_names = ["Laplacian Value", "Brenner Value", "Tenengrad Value", "Gabor Variance"]

        ref_metrics = get_metrics(ref_path)
        comp_metrics = get_metrics(comp_path)

        print(f"{'Metric':<20} {ref_filename:<15} {comp_filename:<15}")
        for name, ref, comp in zip(metrics_names, ref_metrics, comp_metrics):
            print(f"{name:<20} {ref:<15.4f} {comp:<15.4f}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")