"""
iwrs_qc_compare.py
──────────────────────────────────────────────────────────────────────────────
Paired QC comparison: LRC-only TIFFs (old) vs CFA-DNG → SEP TIFFs (new)
Iceland 1985 / IWRS project

Metrics (averaged across all matched pairs):
  1. P97-P3 tonal spread + shadow/highlight clipping %
  2. RMS Tenengrad  (edge sharpness, normalized)
  3. RMS Laplacian  (microcontrast / structure, normalized)

Output: averaged console summary + CSV log

Fix 2026-04-11: OpenCV 4.12.0 AVX2 rejects float32->CV_64F for Sobel/Laplacian.
  Use uint8 input to filter functions instead.
"""

import cv2
import numpy as np
import os
import csv
from datetime import datetime
from pathlib import Path

# Paths
OLD_DIR = r"C:\Users\jaa15\OneDrive\Pictures\#LRC_DEV\ICELAND\WhaleMuseumTiff"
NEW_DIR = r"C:\Users\jaa15\OneDrive\Pictures\#LRC_DEV\ICELAND\IWRS"
LOG_DIR = r"C:\Users\jaa15\OneDrive\PYProjects\Logs"


def load_gray_float(path: str) -> np.ndarray:
    """Load TIFF grayscale. IMREAD_ANYDEPTH prevents silent 16->8 downcast."""
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
    """RMS Tenengrad - Sobel edge sharpness, normalized by pixel count.
    uint8 input required -- OpenCV 4.12.0 AVX2 rejects float32->CV_64F."""
    s  = (img * 255.0).clip(0, 255).astype(np.uint8)
    sx = cv2.Sobel(s, cv2.CV_64F, 1, 0, ksize=3)
    sy = cv2.Sobel(s, cv2.CV_64F, 0, 1, ksize=3)
    return float(np.sqrt(np.mean(sx ** 2 + sy ** 2)))


def rms_laplacian(img: np.ndarray) -> float:
    """RMS Laplacian - second-order gradient, normalized by pixel count.
    uint8 input required -- OpenCV 4.12.0 AVX2 rejects float32->CV_64F."""
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


def numeric_prefix(stem: str) -> str:
    return stem.split("_")[0]


def build_index(folder: str, strip_suffix: str = "") -> dict:
    """Returns {numeric_prefix: Path} for all *.tif in folder root only."""
    index = {}
    for f in Path(folder).glob("*.tif"):
        stem = f.stem
        if strip_suffix and stem.endswith(strip_suffix):
            stem = stem[: -len(strip_suffix)]
        num = numeric_prefix(stem)
        index[num] = f
    return index


def main():
    print("=" * 62)
    print("  IWRS QC Comparison  —  LRC-only vs CFA-DNG + SEP")
    print("=" * 62)

    old_idx = build_index(OLD_DIR, strip_suffix="")
    new_idx = build_index(NEW_DIR, strip_suffix="-Edit")

    matched       = sorted(set(old_idx) & set(new_idx), key=lambda x: int(x))
    unmatched_old = set(old_idx) - set(new_idx)
    unmatched_new = set(new_idx) - set(old_idx)

    print(f"\n  Matched pairs : {len(matched)}")
    if unmatched_old:
        print(f"  Old-only      : {sorted(unmatched_old, key=int)} (skipped)")
    if unmatched_new:
        print(f"  New-only      : {sorted(unmatched_new, key=int)} (skipped)")
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
        print("\nNo pairs processed. Check paths.")
        return

    def avg(lst):  return round(float(np.mean(lst)), 4)
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
    print(f"  {'METRIC':<24} {'OLD':>9} {'NEW':>9} {'DELTA':>9} {'CHANGE':>8}")
    print("-" * 62)

    summary_rows = []
    for label, key in metrics:
        o  = avg(old_acc[key])
        n  = avg(new_acc[key])
        d  = round(n - o, 4)
        pc = pct(old_acc[key], new_acc[key])
        print(f"  {label:<24} {o:>9.4f} {n:>9.4f} {d:>+9.4f} {pc:>8}")
        summary_rows.append({"metric": label, "old_avg": o, "new_avg": n,
                              "delta": d, "pct_change": pc})

    print("=" * 62)
    print(f"\n  Pairs: {len(matched)}  |  Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"    ERR {e}")

    os.makedirs(LOG_DIR, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(LOG_DIR, f"iwrs_qc_compare_{ts}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "old_avg", "new_avg",
                                          "delta", "pct_change"])
        w.writeheader()
        w.writerows(summary_rows)
    print(f"\n  CSV: {csv_path}\n")


if __name__ == "__main__":
    main()
