# ssim_psnr_metrics.py

import os
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from image_utils import get_qc_image_path

def compare_with_reference(image_path, reference_path):
    img1 = cv2.imread(image_path)
    img2 = cv2.imread(reference_path)
    if img1 is None or img2 is None:
        print("Error: One or both images not found.")
        return None

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    ssim_score = ssim(img1_gray, img2_gray)
    psnr_score = psnr(img1_gray, img2_gray)

    print(f"🔍 SSIM: {ssim_score:.4f}")
    print(f"📶 PSNR: {psnr_score:.2f} dB")
    return ssim_score, psnr_score

if __name__ == "__main__":
    try:
        image_file = get_qc_image_path()
        reference_file = os.path.join(os.getcwd(), "QCImages", "QCRef_GT.jpg")
        compare_with_reference(image_file, reference_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")