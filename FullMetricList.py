import cv2
import numpy as np

def calculate_laplacian_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian.var()

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

if __name__ == "__main__":
    img_path = "/workspaces/PhotoQC/ImageQC/_9093103.jpg"
    laplacian_value = calculate_laplacian_sharpness(img_path)
    brenner_value = calculate_brenner_sharpness(img_path)
    tenengrad_value = calculate_tenengrad_sharpness(img_path)
    gabor_variance = calculate_gabor_variance(img_path)

    print(f"Laplacian Value = {laplacian_value}")
    print(f"Brenner Value = {brenner_value}")
    print(f"Tenengrad Value = {tenengrad_value}")
    print(f"Gabor Variance = {gabor_variance}")