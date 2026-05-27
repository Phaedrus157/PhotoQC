"""
suite_paired_compare.py
Paired QC comparison suite. Matches image files between two folders by
numeric filename prefix and reports averaged metrics across all matched pairs.

Metrics (averaged across all matched pairs):
  1. Tonal spread (P97-P3) + shadow/highlight clipping %
  2. RMS Tenengrad sharpness (normalized by pixel count)
  3. RMS Laplacian microcontrast (normalized by pixel count)

Output: averaged console summary + CSV log

Folders: C:/TEMP/QCImages/A  and  C:/TEMP/QCImages/B

Note: OpenCV 4.12.0 AVX2 rejects float32->CV_64F for Sobel/Laplacian;
uint8 input is used for those filter calls.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
import cv2
import numpy as np
import csv
from datetime import datetime
from pathlib import Path

LOG_DIR = r"C:\Users\Public\Documents\PYProjects\Logs"


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


def build_index(folder: str) -> dict:
    """Returns {stem: Path} for all supported image files in folder root. First match wins."""
    exts = ("*.tif", "*.tiff", "*.jpg", "*.jpeg", "*.png")
    index = {}
    for ext in exts:
        for f in Path(folder).glob(ext):
            if f.stem not in index:
                index[f.stem] = f
    return index


def main():
    folder1 = r"C:\TEMP\QCImages\A"
    folder2 = r"C:\TEMP\QCImages\B"

    print("=" * 62)
    print("  Paired QC Comparison")
    print("=" * 62)

    old_idx = build_index(folder1)
    new_idx = build_index(folder2)

    matched       = sorted(set(old_idx) & set(new_idx))
    unmatched_old = set(old_idx) - set(new_idx)
    unmatched_new = set(new_idx) - set(old_idx)

    print(f"\n  Folder 1      : {folder1}")
    print(f"  Folder 2      : {folder2}")
    print(f"  Matched pairs : {len(matched)}")
    if unmatched_old:
        print(f"  Folder1-only  : {sorted(unmatched_old)} (skipped)")
    if unmatched_new:
        print(f"  Folder2-only  : {sorted(unmatched_new)} (skipped)")
    print()

    old_acc = {k: [] for k in ("spread", "clip_lo", "clip_hi", "tenengrad", "laplacian")}
    new_acc = {k: [] for k in ("spread", "clip_lo", "clip_hi", "tenengrad", "laplacian")}
    errors  = []

    for num in matched:
        try:
            om = compute_all(old_idx[num])
            nm = compute_all(new_idx[num])
            for k in old_acc:
                old_acc[k].append(om[k])
                new_acc[k].append(nm[k])
            print(f"  OK #{num:>2}  {old_idx[num].name:<28} <-> {new_idx[num].name}")
        except Exception as e:
            errors.append(f"#{num}: {e}")
            print(f"  ERR #{num:>2}  {e}")

    if not old_acc["spread"]:
        print("\nNo pairs processed. Check folder paths and file naming.")
        return

    def avg(lst):
        return round(float(np.mean(lst)), 4)

    def pct(o, n):
        a = avg(o)
        return f"{((avg(n) - a) / a * 100):+.1f}%" if a != 0 else "N/A"

    metrics = [
        ("Tonal spread (P97-P3)", "spread"),
        ("Shadow clip %",         "clip_lo"),
        ("Highlight clip %",      "clip_hi"),
        ("Tenengrad (sharpness)", "tenengrad"),
        ("Laplacian (structure)", "laplacian"),
    ]

    print("\n" + "=" * 62)
    print(f"  {'METRIC':<24} {'FOLDER1':>9} {'FOLDER2':>9} {'DELTA':>9} {'CHANGE':>8}")
    print("-" * 62)

    summary_rows = []
    for label, key in metrics:
        o  = avg(old_acc[key])
        n  = avg(new_acc[key])
        d  = round(n - o, 4)
        pc = pct(old_acc[key], new_acc[key])
        print(f"  {label:<24} {o:>9.4f} {n:>9.4f} {d:>+9.4f} {pc:>8}")
        summary_rows.append({"metric": label, "folder1_avg": o, "folder2_avg": n,
                              "delta": d, "pct_change": pc})

    print("=" * 62)
    print(f"\n  Pairs: {len(matched)}  |  Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"    ERR {e}")

    os.makedirs(LOG_DIR, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(LOG_DIR, f"paired_compare_{ts}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "folder1_avg", "folder2_avg",
                                          "delta", "pct_change"])
        w.writeheader()
        w.writerows(summary_rows)
    print(f"\n  CSV: {csv_path}\n")


if __name__ == "__main__":
    main()
