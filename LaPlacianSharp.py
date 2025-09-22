import cv2

def calculate_laplacian_sharpness(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Compute Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    variance = laplacian.var()

    return variance

if __name__ == "__main__":
    img_path = "/workspaces/PhotoQC/ImageQC/_9093103.jpg"
    sharpness = calculate_laplacian_sharpness(img_path)
    print(f"Laplacian sharpness (variance): {sharpness}")