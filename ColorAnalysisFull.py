import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000

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

def analyze_color_accuracy_and_white_balance(image_path):
    print("\n=== 🎯 Color Accuracy and White Balance Analysis ===")
    try:
        original_img = Image.open(image_path)
        img_array = np.array(original_img).astype('float32')

        r_avg = np.mean(img_array[:, :, 0])
        g_avg = np.mean(img_array[:, :, 1])
        b_avg = np.mean(img_array[:, :, 2])
        gray_avg = (r_avg + g_avg + b_avg) / 3

        r_gain = gray_avg / r_avg
        g_gain = gray_avg / g_avg
        b_gain = gray_avg / b_avg

        wb_img_array = np.dstack([
            img_array[:, :, 0] * r_gain,
            img_array[:, :, 1] * g_gain,
            img_array[:, :, 2] * b_gain
        ])
        wb_img_array = np.clip(wb_img_array, 0, 255).astype(np.uint8)
        wb_img = Image.fromarray(wb_img_array)

        width, height = original_img.size
        combined_img = Image.new('RGB', (width * 2, height))
        combined_img.paste(original_img, (0, 0))
        combined_img.paste(wb_img, (width, 0))
        combined_img.show(title="Original (Left) vs. White Balanced (Right)")
        print("✅ White-balanced image preview generated. Please close the window to continue.")

        original_avg_srgb = sRGBColor(r_avg / 255, g_avg / 255, b_avg / 255)
        original_avg_lab = convert_color(original_avg_srgb, LabColor)
        white_ref_lab = LabColor(lab_l=100.0, lab_a=0.0, lab_b=0.0)
        delta_e = delta_e_cie2000(original_avg_lab, white_ref_lab)

        print(f"Average RGB       : R:{r_avg:.2f}, G:{g_avg:.2f}, B:{b_avg:.2f}")
        print(f"Delta E (CIEDE2000): {delta_e:.2f}")

        if delta_e <= 1.0:
            print("Conclusion: The color cast is not perceptible to the human eye. Excellent color accuracy.")
        elif delta_e <= 2.0:
            print("Conclusion: The color cast is perceptible with close observation. Very good color accuracy.")
        else:
            print("Conclusion: A significant color cast is present. Color accuracy is low.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    image_path = "QCImages/QCRef.jpg"
    calculate_colorfulness_metric(image_path)
    analyze_tonal_distribution(image_path)
    analyze_color_accuracy_and_white_balance(image_path)
