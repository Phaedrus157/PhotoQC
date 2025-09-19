import os
import numpy as np
from PIL import Image
from brisque import BRISQUE

def calculate_brisque_score(image_path):
    """
    Calculates the BRISQUE (Blind/Referenceless Image Spatial Quality Evaluator) score for a given image.
    Lower scores indicate better perceptual quality (less distortion or blur).
    """
    try:
        # Load image and convert to RGB format
        img = Image.open(image_path).convert("RGB")

        # Convert image to NumPy array for processing
        img_array = np.asarray(img)

        # Initialize BRISQUE scorer (no URL model used)
        scorer = BRISQUE(url=False)

        # Compute BRISQUE score
        score = scorer.score(img_array)

        # Output section: print score and interpretation
        print(f"📉 BRISQUE Score: {score:.2f}")
        print("🔍 Interpretation:")
        print(" - Lower score = higher perceptual quality (sharper, less distorted)")
        print(" - Higher score = lower quality (more blur, noise, or artifacts)")
        print(" - Use scores to compare relative quality across images")

        return score

    except Exception as e:
        print(f"❌ Error calculating BRISQUE score: {e}")
        return None

if __name__ == "__main__":
    # Define path to the image to be evaluated
    image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")

    # Run BRISQUE score calculation
    calculate_brisque_score(image_file)
