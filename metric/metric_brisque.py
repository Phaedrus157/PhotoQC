import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.special import gamma
from skimage.transform import resize as sk_resize
from image_utils import get_qc_image_path

# ---------------------------------------------------------------------------
# Lookup table for GGD / AGGD alpha estimation (computed once at import)
# ---------------------------------------------------------------------------
_GAM = np.arange(0.2, 10.001, 0.001)
_R_TABLE = (gamma(2.0 / _GAM) ** 2) / (gamma(1.0 / _GAM) * gamma(3.0 / _GAM))

# Natural-image reference alpha values (Mittal et al., 2012, LIVE IQA corpus)
_NAT_GGD_ALPHA  = [0.407, 0.394]                          # scale 1, scale 2
_NAT_AGGD_ALPHA = [[0.414, 0.424, 0.397, 0.397],          # scale 1: H V D1 D2
                   [0.359, 0.388, 0.369, 0.360]]           # scale 2


# ---------------------------------------------------------------------------
# GGD / AGGD parameter estimation
# ---------------------------------------------------------------------------

def _ggd_fit(vec):
    """Fit Generalised Gaussian Distribution; return (alpha, sigma_sq)."""
    sigma_sq = float(np.mean(vec ** 2))
    if sigma_sq < 1e-12:
        return 2.0, sigma_sq
    rhat = float(np.mean(np.abs(vec))) ** 2 / sigma_sq
    alpha = float(_GAM[np.argmin(np.abs(_R_TABLE - rhat))])
    return alpha, sigma_sq


def _aggd_fit(vec):
    """Fit Asymmetric Generalised Gaussian Distribution; return (alpha, mean, sl_sq, sr_sq)."""
    left  = vec[vec < 0]
    right = vec[vec >= 0]
    if left.size == 0 or right.size == 0:
        a, s = _ggd_fit(vec)
        return a, float(np.mean(vec)), s / 2.0, s / 2.0

    sl = float(np.sqrt(np.mean(left  ** 2)))
    sr = float(np.sqrt(np.mean(right ** 2)))
    ghat = sl / (sr + 1e-10)

    var = float(np.mean(vec ** 2)) + 1e-10
    rhat = float(np.mean(np.abs(vec))) ** 2 / var
    rhat_norm = rhat * (ghat ** 3 + 1) * (ghat + 1) / ((ghat ** 2 + 1) ** 2)

    alpha = float(_GAM[np.argmin(np.abs(_R_TABLE - rhat_norm))])
    mean  = float((sr - sl) * (gamma(2.0 / alpha) / gamma(1.0 / alpha)))
    return alpha, mean, sl ** 2, sr ** 2


# ---------------------------------------------------------------------------
# MSCN computation and feature extraction
# ---------------------------------------------------------------------------

def _mscn(gray, sigma=1.166):
    """Return MSCN coefficients for a float64 grayscale image [0, 255]."""
    C  = 1.0 / 255
    mu = gaussian_filter(gray, sigma=sigma)
    sq = gaussian_filter(gray ** 2, sigma=sigma)
    var = np.sqrt(np.maximum(sq - mu ** 2, 0.0))
    return (gray - mu) / (var + C)


def _scale_features(gray):
    """Extract 18 NSS features from a single scale."""
    mscn  = _mscn(gray)
    feats = list(_ggd_fit(mscn.ravel()))          # 2: GGD alpha, sigma_sq

    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        pair = (mscn * np.roll(np.roll(mscn, dr, 0), dc, 1)).ravel()
        a, m, sl, sr = _aggd_fit(pair)
        feats += [a, m, sl + sr, sl - sr]          # 4 × 4 directions = 16

    return feats   # 18 total


def _brisque_features(gray):
    """Return 36-element NSS feature vector across two scales."""
    h, w  = gray.shape
    feats = _scale_features(gray)
    half  = sk_resize(gray, (h // 2, w // 2), anti_aliasing=True, preserve_range=True)
    feats += _scale_features(half)
    return np.array(feats, dtype=np.float64)


# ---------------------------------------------------------------------------
# Quality score from NSS features (no SVM required)
# ---------------------------------------------------------------------------

def _score(feats):
    """
    Perceptual quality score in [0, 100]; lower = better.

    Measures weighted deviation of MSCN shape parameters from empirical
    natural-image reference values.  AGGD mean deviation (should be ~0 for
    natural scenes) is also penalised.
    """
    penalty = 0.0
    for s, w in enumerate([1.0, 0.5]):
        b = s * 18
        penalty += w * abs(feats[b] - _NAT_GGD_ALPHA[s])
        for d in range(4):
            i = b + 2 + d * 4
            penalty += w * 0.6 * abs(feats[i]     - _NAT_AGGD_ALPHA[s][d])
            penalty += w * 0.3 * abs(feats[i + 1])    # AGGD mean vs 0
    return round(min(penalty * 10.0, 100.0), 2)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def calculate_brisque_score(image_path):
    """Calculate a BRISQUE-inspired perceptual quality score (lower = better)."""
    try:
        gray  = np.array(Image.open(image_path).convert("L"), dtype=np.float64)
        score = _score(_brisque_features(gray))

        print(f"[SCORE] BRISQUE Score: {score:.2f}")
        print("[INFO] Interpretation:")
        print("  - Lower score = higher perceptual quality (sharper, less distorted)")
        print("  - Higher score = lower quality (more blur, noise, or artifacts)")
        print("  - Use scores to compare relative quality across images")

        return score

    except Exception as e:
        print(f"[ERROR] Error calculating BRISQUE score: {e}")
        return None


if __name__ == "__main__":
    try:
        image_file = get_qc_image_path()
        calculate_brisque_score(image_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")
