# ssim_psnr_metrics.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import glob
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

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

    print(f"[SSIM] SSIM: {ssim_score:.4f}")
    print(f"[PSNR] PSNR: {psnr_score:.2f} dB")
    return ssim_score, psnr_score

if __name__ == "__main__":
    _qc_dir = r"C:\TEMP\QCImages"
    _exts = ['*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg']
    _found = []
    for _ext in _exts:
        _found.extend(glob.glob(os.path.join(_qc_dir, _ext)))
    if len(_found) < 2:
        print(f"Error: Need at least 2 images in {_qc_dir}")
        sys.exit(1)
    image_file = _found[0]
    reference_file = _found[1]
    try:
        compare_with_reference(image_file, reference_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place two valid image files (TIFF, PNG, or JPEG) in C:\\TEMP\\QCImages\\")
