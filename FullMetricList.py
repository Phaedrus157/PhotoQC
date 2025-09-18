# FullMetricList.py

import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import pywt
import piexif
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000

# --- Image Statistics ---
def get_image_statistics(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Error: File not found at {image_path}")
            return

        pil_image = Image.open(image_path)
        width, height = pil_image.size
        megapixels = (width * height) / 1_000_000.0
        file_size_kb = os.path.getsize(image_path) / 1024.0

        # Megapixel label
        if 75 < megapixels < 85:
            mp_label = "80MP HR"
        elif 45 < megapixels < 55:
            mp_label = "50MP HR"
        elif 15 < megapixels < 25:
            mp_label = "20MP"
        else:
            mp_label = "Other"

        # Bit depth and color space
        color_space = pil_image.mode
        if 'L' in color_space:
            bit_depth = 8
        elif 'RGB' in color_space:
            bit_depth = 24
        elif 'RGBA' in color_space:
            bit_depth = 32
        else:
            bit_depth = "unknown"

        # EXIF data
        try:
            exif_dict = piexif.load(image_path)
            camera_model = exif_dict.get("0th", {}).get(piexif.ImageIFD.Make)
            if camera_model:
                camera_model = camera_model.decode('utf-8')

            exposure_time = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ExposureTime)
            if exposure_time and len(exposure_time) == 2:
                exposure_time = f"{exposure_time[0]}/{exposure_time[1]} sec"

            iso = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ISOSpeedRatings)
        except Exception:
            camera_model = "N/A"
            exposure_time = "N/A"
            iso = "N/A"

        # Print attributes
        print("--- Image File Attributes ---")
        print(f"filename = {os.path.basename(image_path)}")
        print(f"pixel dimensions = {width}x{height}")
        print(f"original MP = {mp_label}")
        print(f"filesizeKB = {file_size_kb:.2f}")
        print(f"filesizeMP = {megapixels:.2f}")
        print(f"bit depth = {bit_depth} bits")
        print(f"color space = {color_space}")
        print(f"camera model = {camera_model}")
        print(f"exposure time = {exposure_time}")
        print(f"ISO = {iso}")

    except Exception as e:
        print(f"An error occurred while getting image statistics: {e}")

# --- Sharpness Metrics ---
def calculate_laplacian_variance(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return cv2.Laplacian(image, cv2.CV_64F).var() if image is not None else 0

def calculate_brenner_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return np.sum(np.diff(image, n=2, axis=0) ** 2) if image is not None else 0

def count_canny_edges(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return cv2.countNonZero(cv2.Canny(image, 100, 200)) if image is not None else 0

def calculate_fft_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
    return np.sum(np.abs(np.fft.ifftshift(fshift)))

def calculate_gabor_variance(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    kernel = cv2.getGaborKernel((31, 31), 4.0, 0, 10.0, 0.5, 0, ktype=cv2.CV_64F)
    return np.var(cv2.filter2D(image, cv2.CV_64F, kernel))

def calculate_tenengrad_metric(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    return np.sum(np.sqrt(sobelx**2 + sobely**2)**2)

def calculate_wavelet_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    _, (LH, HL, HH) = pywt.dwt2(image, 'haar')
    return np.sqrt(np.mean(LH**2) + np.mean(HL**2) + np.mean(HH**2))

def calculate_gradient_metric(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    return np.mean(np.sqrt(sobelx**2 + sobely**2))

def calculate_local_variance(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return np.var(convolve(image, np.ones((3, 3)) / 9, mode='reflect')) if image is not None else 0

def calculate_normalized_average_gradient(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    return np.mean(np.sqrt(grad_x**2 + grad_y**2)) / np.mean(image)

def calculate_sobel_sharpness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    return np.sum(np.sqrt(sobelx**2 + sobely**2))

# --- Noise Analysis ---
def analyze_noise(image_path):
    image = cv2.imread(image_path)
    if image is None: return
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y, u, v = yuv[:, :, 0], yuv[:, :, 1], yuv[:, :, 2]
    print("--- Overall Noise Analysis ---")
    print(f"📈 Laplacian Variance: {cv2.Laplacian(y, cv2.CV_64F).var():.2f}")
    print("--- Advanced Noise Analysis ---")
    print(f"📊 Luminance Noise: {np.std(y):.2f}")
    print(f"🎨 Chrominance Noise: {np.std(u) + np.std(v):.2f}")

def calculate_noise_metric(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    denoised = cv2.medianBlur(image, 5)
    noise = image.astype(np.int16) - denoised.astype(np.int16)
    return np.mean(noise**2)

# --- Artifact Analysis ---
def analyze_chromatic_aberration(image_path):
    image = cv2.imread(image_path)
    if image is None: return
    B, G, R = cv2.split(image)
    b_edge = cv2.Canny(B, 50, 150)
    r_edge = cv2.Canny(R, 50, 150)
    print("--- Chromatic Aberration Analysis ---")
    if b_edge.any() and r_edge.any():
        try:
            shift_y, shift_x = np.unravel_index(np.argmax(cv2.matchTemplate(b_edge, r_edge, cv2.TM_CCOEFF_NORMED)), b_edge.shape)
            print(f"Red Channel Shift: {shift_x}")
            print(f"Blue Channel Shift: {shift_y}")
        except:
            print("Could not compute channel shift.")
    else:
        print("Insufficient edge data for analysis.")

def analyze_compression_artifacts(image_path):
    image = cv2.imread(image_path)
    if image is None: return 0
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return np.sum(cv2.absdiff(image, blurred))

# --- Optical Metrics ---
def analyze_lens_distortion(image_path):
    print("Lens distortion analysis requires a grid reference image. Skipping.")

def analyze_vignetting(image_path):
    image = cv2.imread(image_path)
    if image is None: return
    h, w = image.shape[:2]
    center = image[h//2-50:h//2+50, w//2-50:w//2+50]
    corners = [image[:100, :100], image[:100, -100:], image[-100:, :100], image[-100:, -100:]]
    center_brightness = np.mean(center)
    corners_brightness = np.mean([np.mean(c) for c in corners])
    score = (corners_brightness - center_brightness) / center_brightness * 100
    print("--- Vignetting Analysis ---")
    print(f"Center Brightness: {center_brightness:.2f}")
    print(f"Corners Brightness: {corners_brightness:.2f}")
    print(f"💡 Vignetting Score: {score:.2f}%")

# --- Color Analysis ---
def calculate_colorfulness_metric(image_path):
    print("\n=== 🎨 Colorfulness Metric ===")
    image = cv2.imread(image_path)
    if image is None: return
    B, G, R = cv2.split(image.astype("float32"))
    rg = R - G
    yb = 0.5 * (R + G) - B
    score = np.sqrt(np.std(rg)**2 + np.std(yb)**2) + 0.3 * np.sqrt(np.mean(rg)**2 + np.mean(yb)**2)
    print(f"Colorfulness Score: {score:.2f}")

def analyze_tonal_distribution(image_path):
    print("\n=== 🌗 Tonal Distribution Analysis ===")
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    hist, bins = np.histogram(arr, bins=256, range=[0, 255])
    total = arr.size
    print(f"Clipped Shadows: {hist[0]/total*100:.2f}%")
    print(f"Clipped Highlights: {hist[255]/total*100:.2f}%")
    plt.plot(bins[:-1], hist, color='black')
    plt.title("Luminance Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Pixels")
    plt.grid(True)
    plt.show()

def analyze_color_accuracy_and_white_balance(image_path):
    print("\n=== 🎯 Color Accuracy and White Balance Analysis ===")
    img = Image.open(image_path)
    arr = np.array(img).astype('float32')
    r, g, b = np.mean(arr[:, :, 0]), np.mean(arr[:, :, 1]), np.mean(arr[:, :, 2])
    gray = (r + g + b) / 3
    r_gain, g_gain, b_gain = gray / r, gray / g, gray / b
    corrected = np.clip(np.dstack([arr[:, :, 0]*r_gain, arr[:, :, 1]*g_gain, arr[:, :, 2]*b_gain]), 0, 255).astype(np.uint8)
    Image.fromarray(corrected).show()
    original_lab = convert_color(sRGBColor(r/255, g/255, b/255), LabColor)
    white_lab = LabColor(100.0, 0.0, 0.0)
    delta_e = delta_e_cie2000(original_lab, white_lab)
    print(f"Delta E (CIEDE2000): {delta_e:.2f}")

# --- Master Function ---
def run_all_analyses(image_path):
    print("🌟" * 10 + " Full Image Quality Analysis " + "🌟" * 10)
    get_image_statistics(image_path)

    print("\n===== Sharpness and Focus Metrics =====")
    print(f"Laplacian Variance: {calculate_laplacian_variance(image_path):.2f}")
    print(f"Brenner Metric: {calculate_brenner_sharpness(image_path):.2f}")
    print(f"Canny Edge Count: {count_canny_edges(image_path):.2f}")
    print(f"FFT Sharpness: {calculate_fft_sharpness(image_path):.2f}")
    print(f"Gabor Variance: {calculate_gabor_variance(image_path):.2f}")
    print(f"Tenengrad Metric: {calculate_tenengrad_metric(image_path):.2f}")
    print(f"Wavelet Sharpness: {calculate_wavelet_sharpness(image_path):.2f}")
    print(f"Gradient Metric: {calculate_gradient_metric(image_path):.2f}")
    print(f"Local Variance: {calculate_local_variance(image_path):.2f}")
    print(f"Normalized Avg Gradient: {calculate_normalized_average_gradient(image_path):.2f}")
    print(f"Sobel Sharpness: {calculate_sobel_sharpness(image_path):.2f}")

    print("\n===== Noise and Grain Analysis =====")
    analyze_noise(image_path)
    print(f"Noise Metric: {calculate_noise_metric(image_path):.2f}")

    print("\n===== Image Integrity and Artifacts =====")
    analyze_chromatic_aberration(image_path)
    print(f"Compression Artifact Score: {analyze_compression_artifacts(image_path):.2f}")

    print("\n===== Optical and Geometric Metrics =====")
    analyze_lens_distortion(image_path)
    analyze_vignetting(image_path)

    print("\n===== Color Analysis =====")
    calculate_colorfulness_metric(image_path)
    analyze_tonal_distribution(image_path)
    analyze_color_accuracy_and_white_balance(image_path)

    print("\n✅" * 10 + " Full Analysis Complete! " + "✅" * 10)

# --- Entry Point ---
if __name__ == "__main__":
    image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")
    run_all_analyses(image_file)
