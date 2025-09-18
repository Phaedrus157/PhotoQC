import cv2
import numpy as np
import os
import piexif
from PIL import Image
import matplotlib.pyplot as plt

def get_image_statistics(image_path):
    print("\n=== 📷 Image Attribute Summary ===")
    if not os.path.exists(image_path):
        print(f"❌ Error: The image file was not found at {image_path}")
        return

    cv2_image = cv2.imread(image_path)
    if cv2_image is None:
        print("❌ Error: Could not load the image with OpenCV.")
        return

    try:
        pil_image = Image.open(image_path)
    except IOError as e:
        print(f"❌ Error: Could not open the image with Pillow. {e}")
        return

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
    bit_depth = 8 if 'L' in color_space else 24 if 'RGB' in color_space else "unknown"

    try:
        exif_dict = piexif.load(image_path)
        camera_model = exif_dict.get("0th", {}).get(piexif.ImageIFD.Make)
        if camera_model:
            camera_model = camera_model.decode('utf-8')
        exposure_time = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ExposureTime)
        if exposure_time and len(exposure_time) == 2:
            exposure_time = f"{exposure_time[0]}/{exposure_time[1]} sec"
        iso = exif_dict.get("Exif", {}).get(piexif.ExifIFD.ISOSpeedRatings)
    except (KeyError, piexif.InvalidImageDataError, piexif.NoExifDataError):
        camera_model = "N/A"
        exposure_time = "N/A"
        iso = "N/A"

    print(f"Filename         : {os.path.basename(image_path)}")
    print(f"Dimensions       : {width}x{height}")
    print(f"Megapixels       : {megapixels:.2f} MP → {original_mp_label}")
    print(f"File Size        : {file_size_kb:.2f} KB")
    print(f"Bit Depth        : {bit_depth} bits")
    print(f"Color Space      : {color_space}")
    print(f"Camera Model     : {camera_model}")
    print(f"Exposure Time    : {exposure_time}")
    print(f"ISO              : {iso}")

def calculate_colorfulness_metric(image_path):
    print("\n=== 🎨 Colorfulness Metric ===")
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"❌ Error: Image not found at path: {image_path}")
        return

    (B, G, R) = cv2.split(image.astype("float32"))
    rg = R - G
    yb = 0.5 * (R + G) - B
    std_rg = np.std(rg)
    std_yb = np.std(yb)
    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)
    colorfulness = np.sqrt((std_rg ** 2) + (std_yb ** 2)) + 0.3 * np.sqrt((mean_rg ** 2) + (mean_yb ** 2))
    print(f"Colorfulness Score: {colorfulness:.2f}")

def analyze_tonal_distribution(image_path):
    print("\n=== 🌗 Tonal Distribution Analysis ===")
    try:
        img = Image.open(image_path)
        gray_img = img.convert('L')
        img_array = np.array(gray_img)
        total_pixels = img_array.size
        if total_pixels == 0:
            print("❌ Error: The image has no pixels.")
            return

        histogram, bins = np.histogram(img_array, bins=256, range=[0, 255])
        shadow_pixels = histogram[0]
        highlight_pixels = histogram[255]
        shadow_percent = (shadow_pixels / total_pixels) * 100
        highlight_percent = (highlight_pixels / total_pixels) * 100

        print(f"Clipped Shadows   : {shadow_percent:.2f}% of pixels are pure black (value 0)")
        print(f"Clipped Highlights: {highlight_percent:.2f}% of pixels are pure white (value 255)")

        plt.figure(figsize=(10, 6))
        plt.plot(bins[:-1], histogram, color='black')
        plt.title('Luminance Histogram')
        plt.xlabel('Pixel Intensity (0=Black, 255=White)')
        plt.ylabel('Number of Pixels')
        plt.grid(True)
        plt.axvspan(0, 5, color='red', alpha=0.3, label='Shadow Clipping Zone')
        plt.axvspan(250, 255, color='red', alpha=0.3, label='Highlight Clipping Zone')
        plt.legend()
        plt.show()

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    image_path = "QCImages/QCRef.jpg"
    get_image_statistics(image_path)
    calculate_colorfulness_metric(image_path)
    analyze_tonal_distribution(image_path)
