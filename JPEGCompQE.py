# jpeg_quality_estimator.py

import os
from PIL import Image
from image_utils import get_qc_image_path

def estimate_jpeg_quality(image_path):
    try:
        img = Image.open(image_path)
        if img.format != 'JPEG':
            print("Not a JPEG image.")
            return None

        quant_tables = img.quantization
        if quant_tables:
            quality_score = sum([sum(table) for table in quant_tables.values()]) / len(quant_tables)
            print(f"🧮 Estimated JPEG Quality Score: {quality_score:.2f}")
            return quality_score
        else:
            print("No quantization tables found.")
            return None
    except Exception as e:
        print(f"Error reading JPEG quality: {e}")
        return None

if __name__ == "__main__":
    try:
        image_file = get_qc_image_path()
        estimate_jpeg_quality(image_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")