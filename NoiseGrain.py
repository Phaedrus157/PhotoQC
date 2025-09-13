import cv2
import numpy as np

def calculate_noise_metric(image_path: str) -> float:
    """
    Calculates a simple noise metric for a given image using a Laplacian filter.
    
    This function reads an image, converts it to grayscale, and then applies
    a Laplacian filter. The variance of the filtered image is used as a 
    simple metric for noise and grain. A higher value indicates more noise.

    Args:
        image_path: The path to the image file.

    Returns:
        A float representing the calculated noise metric.
    """
    try:
        # Read the image from the specified path
        image = cv2.imread(image_path)
        
        # Check if the image was loaded successfully
        if image is None:
            print(f"Error: Could not read image from {image_path}")
            return -1.0
            
        # Convert the image to grayscale, as noise analysis is often done on a single channel
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply the Laplacian filter to the grayscale image
        # The Laplacian operator is a 2D isotropic filter used to find the second derivative
        # of the image. It is effective in detecting regions of rapid intensity change,
        # which can be a result of noise or grain.
        laplacian_image = cv2.Laplacian(gray_image, cv2.CV_64F)
        
        # Calculate the variance of the filtered image
        # The variance of the Laplacian-filtered image is a common and simple
        # metric for image noise and grain. A higher variance value corresponds
        # to a noisier or grainier image.
        noise_metric = np.var(laplacian_image)
        
        return float(noise_metric)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1.0

# Example usage (for testing the function)
if __name__ == "__main__":
    # You would replace this with the path to your actual image file
    sample_image_path = "QCImages/sample.jpg" 
    
    # Create a dummy image for testing purposes
    # A flat image will have low noise, while a randomized one will be high
    try:
        # Create a simple 100x100 grayscale image with no noise (low variance)
        flat_image = np.zeros((100, 100), dtype=np.uint8)
        cv2.imwrite("QCImages/flat_image.jpg", flat_image)
        
        # Create a noisy image for a high variance score
        noisy_image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        cv2.imwrite("QCImages/noisy_image.jpg", noisy_image)

        # Calculate and print the noise metric for the flat image
        flat_noise = calculate_noise_metric("QCImages/flat_image.jpg")
        print(f"Noise metric for the flat image: {flat_noise:.2f}")

        # Calculate and print the noise metric for the noisy image
        noisy_noise = calculate_noise_metric("QCImages/noisy_image.jpg")
        print(f"Noise metric for the noisy image: {noisy_noise:.2f}")

    except Exception as e:
        print(f"Error creating test images: {e}")
