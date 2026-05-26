import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import glob
import numpy as np

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
    _qc_dir = r"C:\TEMP\QCImages"
    _exts = ['*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg']
    _found = []
    for _ext in _exts:
        _found.extend(glob.glob(os.path.join(_qc_dir, _ext)))
    if len(_found) < 2:
        print(f"Error: Need at least 2 images in {_qc_dir}")
        sys.exit(1)
    ref_path = _found[0]
    comp_path = _found[1]

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
