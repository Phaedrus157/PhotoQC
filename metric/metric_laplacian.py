import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2

def calculate_laplacian_sharpness(image_path):
    """
    Calculates image sharpness using the variance of the Laplacian.

    A higher variance value indicates a sharper image with more detail.
    A lower variance value indicates a blurrier image.

    Threshold interpretation:
        score < 100:       Blurry — likely reject
        score 100 to 300:  Acceptable — review carefully
        score > 300:       Sharp — likely accept

    Parameters:
        image_path (str): The full path to the image file.

    Returns:
        float: The variance of the Laplacian.
    """
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: The image file was not found at {image_path}")

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # If the image failed to load, return an error
    if image is None:
        raise ValueError("Error: Could not load the image. Check file integrity.")

    # Apply the Laplacian filter and calculate the variance
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()

    return laplacian_var

if __name__ == "__main__":
    from image_utils import get_qc_image_path
    img_path = get_qc_image_path()

    try:
        sharpness_score = calculate_laplacian_sharpness(img_path)
        print(f"Laplacian sharpness score for {os.path.basename(img_path)}: {sharpness_score:.2f}")

        if sharpness_score < 100:
            print("Interpretation: Blurry — likely reject")
        elif sharpness_score <= 300:
            print("Interpretation: Acceptable — review carefully")
        else:
            print("Interpretation: Sharp — likely accept")

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
