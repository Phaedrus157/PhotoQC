"""
suite_paired_compare.py
Single-pair QC comparison. Loads the first two image files found in
C:/TEMP/QCImages by extension priority (tif > tiff > jpg > jpeg > png)
and reports a side-by-side metric delta table.

Metrics:
  1. Tonal spread (P97-P3) + shadow/highlight clipping %
  2. RMS Tenengrad sharpness (normalized by pixel count)
  3. RMS Laplacian microcontrast (normalized by pixel count)

Note: OpenCV 4.12.0 AVX2 rejects float32->CV_64F for Sobel/Laplacian;
uint8 input is used for those filter calls.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np
from pathlib import Path

QC_DIR = r"C:\TEMP\QCImages"


def load_gray_float(path: str) -> np.ndarray:
    """Load image as grayscale float. IMREAD_ANYDEPTH prevents silent 16->8 downcast."""
    img = cv2.imread(path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"Cannot load: {path}")
    max_val = 65535.0 if img.dtype == np.uint16 else 255.0
    return img.astype(np.float32) / max_val


def tonal_metrics(img: np.ndarray) -> tuple:
    """P97-P3 spread, shadow clipping %, highlight clipping %."""
    p3      = float(np.percentile(img, 3))
    p97     = float(np.percentile(img, 97))
    clip_lo = float(np.mean(img <= 0.0)) * 100.0
    clip_hi = float(np.mean(img >= 1.0)) * 100.0
    return round(p97 - p3, 4), round(clip_lo, 3), round(clip_hi, 3)


def rms_tenengrad(img: np.ndarray) -> float:
    """RMS Tenengrad sharpness, normalized by pixel count."""
    s  = (img * 255.0).clip(0, 255).astype(np.uint8)
    sx = cv2.Sobel(s, cv2.CV_64F, 1, 0, ksize=3)
    sy = cv2.Sobel(s, cv2.CV_64F, 0, 1, ksize=3)
    return float(np.sqrt(np.mean(sx ** 2 + sy ** 2)))


def rms_laplacian(img: np.ndarray) -> float:
    """RMS Laplacian microcontrast, normalized by pixel count."""
    s = (img * 255.0).clip(0, 255).astype(np.uint8)
    return float(np.sqrt(np.mean(cv2.Laplacian(s, cv2.CV_64F) ** 2)))


def compute_all(path: Path) -> dict:
    img = load_gray_float(str(path))
    spread, clip_lo, clip_hi = tonal_metrics(img)
    return {
        "spread":    spread,
        "clip_lo":   clip_lo,
        "clip_hi":   clip_hi,
        "tenengrad": round(rms_tenengrad(img), 3),
        "laplacian": round(rms_laplacian(img), 3),
    }


def find_images(folder: str) -> list:
    """Return files in folder ordered by extension priority: tif > tiff > jpg > jpeg > png."""
    exts = ("*.tif", "*.tiff", "*.jpg", "*.jpeg", "*.png")
    found = []
    for ext in exts:
        found.extend(Path(folder).glob(ext))
    return found


def main():
    found = find_images(QC_DIR)
    if len(found) < 2:
        print(f"Error: Need at least 2 images in {QC_DIR}")
        sys.exit(1)

    ref_path = found[0]
    cmp_path = found[1]

    print("=" * 62)
    print("  Paired QC Comparison")
    print("=" * 62)
    print(f"\n  FILE1 : {ref_path.name}")
    print(f"  FILE2 : {cmp_path.name}")
    print()

    ref_m = compute_all(ref_path)
    cmp_m = compute_all(cmp_path)

    def pct(o, n):
        return f"{((n - o) / o * 100):+.1f}%" if o != 0 else "N/A"

    metrics = [
        ("Tonal spread (P97-P3)", "spread"),
        ("Shadow clip %",         "clip_lo"),
        ("Highlight clip %",      "clip_hi"),
        ("Tenengrad (sharpness)", "tenengrad"),
        ("Laplacian (structure)", "laplacian"),
    ]

    print("=" * 62)
    print(f"  {'METRIC':<24} {'FILE1':>9} {'FILE2':>9} {'DELTA':>9} {'CHANGE':>8}")
    print("-" * 62)

    for label, key in metrics:
        o  = ref_m[key]
        n  = cmp_m[key]
        d  = round(n - o, 4)
        pc = pct(o, n)
        print(f"  {label:<24} {o:>9.4f} {n:>9.4f} {d:>+9.4f} {pc:>8}")

    print("=" * 62)


if __name__ == "__main__":
    main()
