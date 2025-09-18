import cv2
import numpy as np
import os
import glob

def calculate_colorfulness_metric(image_path):
    """
    Calculates the Hasler and Suesstrunk colorfulness metric for a color image.

    Args:
        image_path (str): The full path to the input image file.

    Returns:
        float: The colorfulness score. A higher value indicates a more colorful image.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    # Read the image in color
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Use float32 to reduce memory usage
    (B, G, R) = cv2.split(image.astype("float32"))

    # Calculate the opponent color channels
    rg = R - G
    yb = 0.5 * (R + G) - B

    # Compute the mean and standard deviation of both channels
    std_rg = np.std(rg)
    std_yb = np.std(yb)
    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)

    # Combine the standard deviations and means to calculate the colorfulness score
    colorfulness = np.sqrt((std_rg ** 2) + (std_yb ** 2)) + 0.3 * np.sqrt((mean_rg ** 2) + (mean_yb ** 2))
    
    return colorfulness

if __name__ == "__main__":
    image_directory = "QCImages"
    image_files = glob.glob(os.path.join(image_directory, "*.jpg")) + glob.glob(os.path.join(image_directory, "*.png"))
    
    if not image_files:
        print(f"No image files found in the '{image_directory}' directory.")
    else:
        print(f"Found {len(image_files)} image(s) to analyze.")
        print("---")
        for img_path in image_files:
            file_name = os.path.basename(img_path)
            
            try:
                colorfulness_score = calculate_colorfulness_metric(img_path)
                
                print(f"Image: {file_name}")
                print(f"  Colorfulness Score = {colorfulness_score:.2f}")
                print("---")
            except Exception as e:
                print(f"An error occurred while processing {file_name}: {e}")
