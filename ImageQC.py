import cv2
import os
import sys
import piexif
import numpy as np
from PIL import Image
from scipy import fftpack, ndimage
from skimage import filters
from image_utils import get_qc_image_path

# --- Image Path ---
try:
    image_path = get_qc_image_path()
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading image: {e}")
    sys.exit(1)

# --- Image Statistics ---
def get_image_statistics(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return {}

    cv2_image = cv2.imread(image_path)
    pil_image = Image.open(image_path)
    width, height = pil_image.size
    megapixels = (width * height) / 1_000_000.0

    if 75 < megapixels < 85:
        original_mp_label = "80MP HR"
    elif 45 < megapixels < 55:
        original_mp_label = "50MP HR"
    elif 15 < megapixels < 25:
        original_mp_label = "20MP"
    else:
        original_mp_label = "Other"

    file_size_kb = os.path.getsize(image_path) / 1024.0
    color_space = pil_image.mode
    bit_depth = 8 if color_space == 'L' else 24 if color_space == 'RGB' else 32 if color_space == 'RGBA' else "unknown"

    try:
        exif_dict = piexif.load(image_path)
        camera_model = exif_dict.get("0th", {}).get(piexif.ImageIFD.Make)
        camera_model = camera_model.decode('utf-8') if camera_model else "N/A"
        exposure_time = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ExposureTime)
        exposure_time = f"{exposure_time[0]}/{exposure_time[1]} sec" if exposure_time else "N/A"
        iso = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ISOSpeedRatings) or "N/A"
    except Exception:
        camera_model = exposure_time = iso = "N/A"

    return {
        "filename": os.path.basename(image_path),
        "dimensions": f"{width}x{height}",
        "original_mp": original_mp_label,
        "filesize_kb": round(file_size_kb, 2),
        "megapixels": round(megapixels, 2),
        "bit_depth": f"{bit_depth} bits",
        "color_space": color_space,
        "camera_model": camera_model,
        "exposure_time": exposure_time,
        "ISO": iso
    }

# --- Analysis Functions ---
def analyze_tonal_distribution(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0,256])
    return {"tonal_distribution": hist.flatten().tolist()}

def analyze_noise(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noise = np.std(gray - cv2.GaussianBlur(gray, (3,3), 0))
    return {"noise_std_dev": round(noise, 4)}

def analyze_chromatic_aberration(image):
    b, g, r = cv2.split(image)
    diff_rg = cv2.absdiff(r, g)
    diff_gb = cv2.absdiff(g, b)
    aberration_score = np.mean(diff_rg + diff_gb)
    return {"chromatic_aberration_score": round(aberration_score, 4)}

def analyze_lens_distortion(image):
    edges = cv2.Canny(image, 100, 200)
    distortion_score = np.mean(edges)
    return {"lens_distortion_score": round(distortion_score, 4)}

def analyze_vignetting(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    center = gray[gray.shape[0]//4:3*gray.shape[0]//4, gray.shape[1]//4:3*gray.shape[1]//4]
    vignetting_score = np.mean(center) / np.mean(gray)
    return {"vignetting_score": round(vignetting_score, 4)}

def analyze_compression_artifacts(image):
    dct = cv2.dct(np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)))
    artifact_score = np.mean(np.abs(dct))
    return {"compression_artifact_score": round(artifact_score, 4)}

def calculate_brenner_sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    shifted = np.roll(gray, -1, axis=0)
    brenner = np.sum((gray - shifted)**2)
    return {"brenner_sharpness": round(brenner, 4)}

def count_canny_edges(image):
    edges = cv2.Canny(image, 100, 200)
    return {"canny_edge_count": int(np.sum(edges > 0))}

def calculate_colorfulness_metric(image):
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.abs(R - G)
    yb = np.abs(0.5 * (R + G) - B)
    std_root = np.sqrt(np.std(rg)**2 + np.std(yb)**2)
    mean_root = np.sqrt(np.mean(rg)**2 + np.mean(yb)**2)
    return {"colorfulness": round(std_root + 0.3 * mean_root, 4)}

def calculate_fft_sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f = fftpack.fft2(gray)
    fshift = fftpack.fftshift(f)
   _spectrum = 20 * np.log(np.abs(fshift))
    return {"fft_sharpness": round(np.mean(magnitude_spectrum), 4)}

def calculate_gabor_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gabor_kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
    filtered = cv2.filter2D(gray, cv2.CV_8UC3, gabor_kernel)
    return {"gabor_variance": round(np.var(filtered), 4)}

def calculate_gradient_metric(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   _x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    return {"gradient_metric": round(np.mean(gradient_magnitude), 4)}

def calculate_local_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    local_var = ndimage.generic_filter(gray, np.var, size=5)
    return {"local_variance": round(np.mean(local_var), 4)}

def calculate_noise_metric(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noise_metric = np.var(gray - cv2.medianBlur(gray, 3))
    return {"noise_metric": round(noise_metric, 4)}

def calculate_normalized_average_gradient(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad = np.gradient(gray.astype("float"))
    mag = np.sqrt(grad[0]**2 + grad[1]**2)
    return {"normalized_avg_gradient": round(np.mean(mag) / 255.0, 4)}

def calculate_sobel_sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel = filters.sobel(gray)
    return {"sobel_sharpness": round(np.mean(sobel), 4)}

def calculate_tenengrad_metric(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    fm = gx**2 + gy**2
    return {"tenengrad_metric": round(np.mean(fm), 4)}

def calculate_wavelet_sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coeffs = fftpack.dct(gray.astype("float"))
    return {"wavelet_sharpness": round(np.mean(np.abs(coeffs)), 4)}

def analyze_color_accuracy_and_white_balance(image):
    avg_color_per_row = np.mean(image, axis=0)
    avg_colors = np.mean(avg_color_per_row, axis=0)
    return {
        "avg_red": round(avg_colors[2], 2),
        "avg_green": round(avg_colors[1], 2),
        "avg_blue": round(avg_colors[0], 2)
    }

# --- Main Execution ---
if __name__ == "__main__":
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        sys.exit(1)

    results = {}
    results.update(get_image_statistics(image_path))
    results.update(analyze_tonal_distribution(image))
    results.update(analyze_noise(image))
    results.update(analyze_chromatic_aberration(image))
    results.update(analyze_lens_distortion(image))
    results.update(analyze_vignetting(image))
    results.update(analyze_compression_artifacts(image))
    results.update(calculate_brenner_sharpness(image))
    results.update(count_canny_edges(image))
    results.update(calculate_colorfulness_metric(image))
    results.update(calculate_fft_sharpness(image))
    results.update(calculate_gabor_variance(image))
    results.update(calculate_gradient_metric(image))
    results.update(calculate_local_variance(image))
    results.update(calculate_noise_metric(image))
    results.update(calculate_normalized_average_gradient(image))
    results.update(calculate_sobel_sharpness(image))
    results.update(calculate_tenengrad_metric(image))
    results.update(calculate_wavelet_sharpness(image))
    results.update(analyze_color_accuracy_and_white_balance(image))

    print("\n--- Image Quality Analysis Report ---")
    for key, value in results.items():
        print(f"{key}: {value}")
