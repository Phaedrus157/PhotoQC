# brisque_metric.py

import os
import numpy as np
from PIL import Image
from brisque import BRISQUE

def calculate_brisque_score(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img_array = np.asarray(img)
        scorer = BRISQUE(url=False)
        score = scorer.score(img_array)
        print(f"📉 BRISQUE Score: {score:.2f}")
        return score
    except Exception as e:
        print(f"Error calculating BRISQUE score: {e}")
        return None

if __name__ == "__main__":
    image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")
    calculate_brisque_score(image_file)
