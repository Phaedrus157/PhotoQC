import sys
import os
import cv2
import numpy as np
import exifread
from PIL import Image
from scipy.signal import convolve2d
from scipy.ndimage import convolve
import pywt

def get_image_statistics(image_path):
    """Gathers and prints file attributes and EXIF data."""
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            
        print("--- Image File Attributes ---")
        filename = os.path.basename(image_path)
        img = Image.open(image_path)
        width, height = img.size
        filesize_bytes = os.path.getsize(image_path)
        
        print(f"filename = {filename}")
        print(f"pixel dimensions = {width}x{height}")
        print(f"filesizeKB = {filesize_bytes / 1024:.2f}")
        
        if 'Image Tag 0x011A' in tags:
            print(f"camera model = {tags['Image Tag 0x011A']}")
        if 'EXIF ExposureTime' in tags:
            print(f"exposure time = {tags['EXIF ExposureTime']}")
        if 'EXIF ISOSpeedRatings' in tags:
            print(f"ISO = {tags['EXIF ISOSpeedRatings']}")
        
    except Exception as e:
        print(f"An error occurred while getting image statistics: {e}")

# --- Sharpness and Focus Metrics ---
def calculate_laplacian_variance(image_path):
    """Calculates sharpness using Laplacian variance."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    return cv2.Laplacian(image, cv2.CV_64F).var()

def calculate_brenner_sharpness(image_path):
    """Calculates sharpness using the Brenner metric."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    diff = np.diff(image, n=2, axis=0)
    return np.sum(diff ** 2)

def count_canny_edges(image_path):
    """Counts edges using the Canny algorithm as a sharpness metric."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    edges = cv2.Canny(image, 100, 200)
    return cv2.countNonZero(edges)

def calculate_fft_sharpness(image_path):
    """Calculates sharpness from the FFT's high-frequency energy."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
    fshift = np.fft.ifftshift(fshift)
    fft_sharpness_score = np.sum(np.abs(fshift))
    return fft_sharpness_score

def calculate_gabor_variance(image_path):
    """Calculates sharpness using the variance of Gabor filter responses."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    gabor_kernel = cv2.getGaborKernel((31, 31), 4.0, 0, 10.0, 0.5, 0, ktype=cv2.CV_64F)
    filtered = cv2.filter2D(image, cv2.CV_64F, gabor_kernel)
    return np.var(filtered)

def calculate_tenengrad_metric(image_path):
    """Calculates sharpness using the Tenengrad method (Sobel operator)."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    return np.sum(grad_mag**2)

def calculate_wavelet_sharpness(image_path):
    """Calculates sharpness using wavelet transform coefficients."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    coeffs = pywt.dwt2(image, 'haar')
    LH, HL, HH = coeffs[1]
    return np.sqrt(np.mean(LH**2) + np.mean(HL**2) + np.mean(HH**2))

def calculate_gradient_metric(image_path):
    """Calculates sharpness based on the average gradient magnitude."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    return np.mean(grad_mag)

def calculate_local_variance(image_path):
    """Calculates sharpness from the variance of local pixel intensities."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    local_variance_map = convolve(image, np.ones((3, 3)) / 9, mode='reflect')
    return np.var(local_variance_map)

def calculate_normalized_average_gradient(image_path):
    """Calculates a normalized average gradient as a sharpness metric."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    avg_grad = np.mean(np.sqrt(grad_x**2 + grad_y**2))
    return avg_grad / np.mean(image)

def calculate_sobel_sharpness(image_path):
    """Calculates sharpness based on the Sobel edge intensity score."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    return np.sum(grad_mag)

# --- Noise and Grain ---
def analyze_noise(image_path):
    """Analyzes noise using luminance and chrominance channels."""
    image = cv2.imread(image_path)
    if image is None: return
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel = yuv_image[:, :, 0]
    u_channel = yuv_image[:, :, 1]
    v_channel = yuv_image[:, :, 2]
    
    luminance_noise = np.std(y_channel)
    chrominance_noise = np.std(u_channel) + np.std(v_channel)
    
    print("--- Overall Noise Analysis ---")
    print(f"📈 Overall Noise Metric (Laplacian Variance): {cv2.Laplacian(y_channel, cv2.CV_64F).var():.2f}")
    print("\n--- Advanced Noise Analysis ---")
    print(f"📊 Luminance Noise (Y-channel): {luminance_noise:.2f}")
    print(f"🎨 Chrominance Noise (Cb/Cr-channels): {chrominance_noise:.2f}")
    
    if luminance_noise > chrominance_noise:
        print("Analysis Conclusion: Luminance noise is more dominant. The image appears grainy.")
    else:
        print("Analysis Conclusion: Chrominance noise is more dominant. The image appears blotchy.")

def calculate_noise_metric(image_path):
    """Calculates a simple noise metric based on median filtering and subtraction."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None: return 0
    
    denoised = cv2.medianBlur(image, 5)
    noise = np.subtract(image.astype(np.int16), denoised.astype(np.int16))
    noise_power = np.mean(noise**2)
    return noise_power

# --- Image Integrity and Artifacts ---
def analyze_chromatic_aberration(image_path):
    """Analyzes chromatic aberration by measuring channel shifts."""
    image = cv2.imread(image_path)
    if image is None: return
    B, G, R = cv2.split(image)
    b_edge = cv2.Canny(B, 50, 150)
    r_edge = cv2.Canny(R, 50, 150)
    
    shift_x, shift_y = 0, 0
    if b_edge.any() and r_edge.any():
        try:
            shift_y, shift_x = np.unravel_index(np.argmax(cv2.matchTemplate(b_edge, r_edge, cv2.TM_CCOEFF_NORMED)), b_edge.shape)
        except Exception:
            pass
    
    print("--- Chromatic Aberration Analysis ---")
    print(f"Red Channel Shift (pixels): {shift_x}")
    print(f"Blue Channel Shift (pixels): {shift_y}")

def analyze_compression_artifacts(image_path):
    """Analyzes artifacts using a simple blur and difference metric."""
    image = cv2.imread(image_path)
    if image is None: return 0
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    diff = cv2.absdiff(image, blurred_image)
    return np.sum(diff)

# --- Optical and Geometric Metrics ---
def analyze_lens_distortion(image_path):
    """A basic check for lens distortion by analyzing straight lines."""
    print("Lens distortion analysis requires a known reference image (e.g., a grid pattern).")
    print("This metric is a placeholder and cannot be calculated on an arbitrary image.")

def analyze_vignetting(image_path):
    """Analyzes vignetting by comparing center and corner brightness."""
    image = cv2.imread(image_path)
    if image is None: return
    height, width, _ = image.shape
    center_region = image[height//2 - 50:height//2 + 50, width//2 - 50:width//2 + 50]
    center_brightness = np.mean(center_region)
    corners_brightness = np.mean([
        np.mean(image[:100, :100]),
        np.mean(image[:100, -100:]),
        np.mean(image[-100:, :100]),
        np.mean(image[-100:, -100:])
    ])
    
    vignetting_score = (corners_brightness - center_brightness) / center_brightness * 100
    
    print("--- Vignetting Analysis ---")
    print(f"Center Brightness: {center_brightness:.2f}")
    print(f"Corners Brightness: {corners_brightness:.2f}")
    print(f"💡 Vignetting Score (Light Falloff): {vignetting_score:.2f}%")
    if vignetting_score > 0:
        print("Conclusion: Corners are brighter than the center (Reverse Vignetting).")
    else:
        print("Conclusion: Corners are darker than the center (Normal Vignetting).")

# --- Master function to run all analyses ---
def run_all_analyses(image_path):
    """
    Main function to run all image quality analysis routines.
    """
    if not os.path.exists(image_path):
        print(f"❌ Error: The file '{image_path}' was not found.")
        return

    print("🌟" * 10 + " Full Image Quality Analysis " + "🌟" * 10)
    
    get_image_statistics(image_path)

    print("\n" + "=" * 5 + " Sharpness and Focus Metrics " + "=" * 5)
    print(f"Laplacian Variance: {calculate_laplacian_variance(image_path):.2f}")
    print(f"Brenner Metric: {calculate_brenner_sharpness(image_path):.2f}")
    print(f"Canny Edge Count: {count_canny_edges(image_path):.2f}")
    print(f"FFT Sharpness: {calculate_fft_sharpness(image_path):.2f}")
    print(f"Gabor Variance: {calculate_gabor_variance(image_path):.2f}")
    print(f"Tenengrad Metric: {calculate_tenengrad_metric(image_path):.2f}")
    print(f"Wavelet Sharpness: {calculate_wavelet_sharpness(image_path):.2f}")
    print(f"Gradient Metric: {calculate_gradient_metric(image_path):.2f}")
    print(f"Local Variance: {calculate_local_variance(image_path):.2f}")
    print(f"Normalized Average Gradient: {calculate_normalized_average_gradient(image_path):.2f}")
    print(f"Sobel Sharpness: {calculate_sobel_sharpness(image_path):.2f}")
    print("-" * 40)

    print("\n" + "=" * 5 + " Noise and Grain Analysis " + "=" * 5)
    analyze_noise(image_path)
    print(f"Noise Metric (Denoised Diff): {calculate_noise_metric(image_path):.2f}")
    print("-" * 40)

    print("\n" + "=" * 5 + " Image Integrity and Artifacts " + "=" * 5)
    analyze_chromatic_aberration(image_path)
    print(f"Compression Artifact Score: {analyze_compression_artifacts(image_path):.2f}")
    print("-" * 40)
    
    print("\n" + "=" * 5 + " Optical and Geometric Metrics " + "=" * 5)
    analyze_lens_distortion(image_path)
    analyze_vignetting(image_path)
    print("-" * 40)

    print("\n" + "✅" * 10 + " Full Analysis Complete! " + "✅" * 10)

if __name__ == "__main__":
    image_file = os.path.join("QCImages", "QCRef.jpg")
    run_all_analyses(image_file)