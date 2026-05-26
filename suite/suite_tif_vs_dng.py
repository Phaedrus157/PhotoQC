"""
suite_tif_vs_dng.py
Compares two TIFF images across quality metrics and prints a side-by-side
delta table. Metrics: Laplacian sharpness, Tenengrad sharpness, luminance
noise, dynamic range, shadow clipping, highlight clipping, SSIM, PSNR.
A log file is saved to the Logs directory.

Usage: py suite_tif_vs_dng.py <ref_path> <compare_path>
"""

import cv2
import numpy as np
import os
import sys
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

LOG_DIR = r"C:\Users\Public\Documents\PYProjects\Logs"


def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"ERROR: Could not load {path}")
        sys.exit(1)
    return img


def normalize(img):
    img_f = img.astype(np.float64)
    max_val = 65535.0 if img.dtype == np.uint16 else 255.0
    return img_f / max_val


def to_gray_norm(img_norm):
    if len(img_norm.shape) == 2:
        return img_norm
    return np.mean(img_norm, axis=2)


def metric_laplacian(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    return cv2.Laplacian(img8, cv2.CV_64F).var()


def metric_tenengrad(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    gx = cv2.Sobel(img8, cv2.CV_64F, 1, 0)
    gy = cv2.Sobel(img8, cv2.CV_64F, 0, 1)
    return np.mean(gx**2 + gy**2)


def metric_noise_luminance(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    denoised = cv2.medianBlur(img8, 5)
    noise = img8.astype(np.int16) - denoised.astype(np.int16)
    return np.std(noise)


def metric_dynamic_range(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    return float(np.max(img8) - np.min(img8))


def metric_shadow_clip(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    hist = cv2.calcHist([img8], [0], None, [256], [0, 256])
    return float(hist[0][0] / img8.size * 100)


def metric_highlight_clip(img_gray):
    img8 = (img_gray * 255).astype(np.uint8)
    hist = cv2.calcHist([img8], [0], None, [256], [0, 256])
    return float(hist[255][0] / img8.size * 100)


def metric_ssim_cross(ref_gray, new_gray):
    ref8 = (ref_gray * 255).astype(np.uint8)
    new8 = (new_gray * 255).astype(np.uint8)
    h = min(ref8.shape[0], new8.shape[0])
    w = min(ref8.shape[1], new8.shape[1])
    return float(ssim(ref8[:h, :w], new8[:h, :w]))


def metric_psnr_cross(ref_gray, new_gray):
    ref8 = (ref_gray * 255).astype(np.uint8)
    new8 = (new_gray * 255).astype(np.uint8)
    h = min(ref8.shape[0], new8.shape[0])
    w = min(ref8.shape[1], new8.shape[1])
    try:
        return float(psnr(ref8[:h, :w], new8[:h, :w]))
    except Exception:
        return 0.0


def winner(ref_val, new_val, higher_is_better=True):
    if abs(ref_val - new_val) < 0.001:
        return "EQUAL"
    if higher_is_better:
        return "REF" if ref_val > new_val else "COMPARE"
    else:
        return "REF" if ref_val < new_val else "COMPARE"


def main():
    if len(sys.argv) < 3:
        print("Usage: py suite_tif_vs_dng.py <ref_path> <compare_path>")
        sys.exit(1)

    ref_path = sys.argv[1]
    new_path = sys.argv[2]
    log_file = os.path.join(LOG_DIR, f"tif_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    print("\nLoading images...")
    ref_img = load_image(ref_path)
    new_img = load_image(new_path)

    ref_norm = normalize(ref_img)
    new_norm = normalize(new_img)
    ref_gray = to_gray_norm(ref_norm)
    new_gray = to_gray_norm(new_norm)

    ref_info = f"{ref_img.shape[1]}x{ref_img.shape[0]} {ref_img.dtype}"
    new_info = f"{new_img.shape[1]}x{new_img.shape[0]} {new_img.dtype}"

    print(f"  REF : {os.path.basename(ref_path)} [{ref_info}]")
    print(f"  CMP : {os.path.basename(new_path)} [{new_info}]")

    print("\nCalculating metrics...")
    results = []

    def add(name, ref_val, new_val, higher_is_better=True, unit=""):
        w = winner(ref_val, new_val, higher_is_better)
        results.append((name, ref_val, new_val, w, unit))

    add("Laplacian Sharpness",  metric_laplacian(ref_gray),            metric_laplacian(new_gray),            True,  "")
    add("Tenengrad Sharpness",  metric_tenengrad(ref_gray),            metric_tenengrad(new_gray),            True,  "")
    add("Noise (Luminance)",    metric_noise_luminance(ref_gray),      metric_noise_luminance(new_gray),      False, "std")
    add("Dynamic Range",        metric_dynamic_range(ref_gray),        metric_dynamic_range(new_gray),        True,  "pts")
    add("Shadow Clipping",      metric_shadow_clip(ref_gray),          metric_shadow_clip(new_gray),          False, "%")
    add("Highlight Clipping",   metric_highlight_clip(ref_gray),       metric_highlight_clip(new_gray),       False, "%")
    add("SSIM (cross-image)",   metric_ssim_cross(ref_gray, new_gray), metric_ssim_cross(ref_gray, new_gray), True,  "")
    add("PSNR (cross-image)",   metric_psnr_cross(ref_gray, new_gray), metric_psnr_cross(ref_gray, new_gray), True,  "dB")

    header = f"\n{'Metric':<25} {'REF':>14} {'COMPARE':>14} {'WINNER':<14}"
    divider = "-" * 70

    lines = []
    lines.append(f"REF : {ref_path}")
    lines.append(f"CMP : {new_path}")
    lines.append(f"Run : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"REF dims/depth : {ref_info}")
    lines.append(f"CMP dims/depth : {new_info}")
    lines.append(divider)
    lines.append(header)
    lines.append(divider)

    for name, ref_val, new_val, w, unit in results:
        line = f"{name:<25} {ref_val:>13.4f}{unit} {new_val:>13.4f}{unit} {w:<14}"
        lines.append(line)

    lines.append(divider)
    lines.append("\nNOTE: SSIM and PSNR are cross-image similarity scores (ref vs compare).")

    output = "\n".join(lines)
    print(output)

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\nLog saved: {log_file}")


if __name__ == "__main__":
    main()
