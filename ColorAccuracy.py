import sys
from PIL import Image
import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from image_utils import get_qc_image_path

def analyze_color_accuracy_and_white_balance(image_path):
    """
    Performs a simple white balance correction on an image and calculates
    the Delta E of the original's average color against a white reference.

    Args:
        image_path (str): The path to the image file.
    """
    try:
        # Load the image
        original_img = Image.open(image_path)
        print(f"✅ Successfully loaded image: {image_path}")
        
        # --- White Balance Analysis (Gray World Algorithm) ---
        print("\n--- White Balance Analysis ---")
        img_array = np.array(original_img).astype('float32')

        # Calculate the average color of the image
        r_avg = np.mean(img_array[:, :, 0])
        g_avg = np.mean(img_array[:, :, 1])
        b_avg = np.mean(img_array[:, :, 2])
        
        # Determine the average grayscale value
        gray_avg = (r_avg + g_avg + b_avg) / 3

        # Calculate the gain for each channel to neutralize the average color
        r_gain = gray_avg / r_avg
        g_gain = gray_avg / g_avg
        b_gain = gray_avg / b_avg
        
        # Apply the gain to the original image array
        wb_img_array = np.dstack([
            img_array[:, :, 0] * r_gain,
            img_array[:, :, 1] * g_gain,
            img_array[:, :, 2] * b_gain
        ])
        
        # Clip values to the valid 0-255 range and convert back to uint8
        wb_img_array = np.clip(wb_img_array, 0, 255).astype(np.uint8)
        wb_img = Image.fromarray(wb_img_array)

        # Create a new, larger image to hold both the original and white-balanced images
        width, height = original_img.size
        combined_img = Image.new('RGB', (width * 2, height))
        combined_img.paste(original_img, (0, 0))
        combined_img.paste(wb_img, (width, 0))
        
        combined_img.show(title="Original (Left) vs. White Balanced (Right)")
        print("✅ White-balanced image preview generated. Please close the window to continue.")

        # --- Delta E Color Accuracy Analysis ---
        print("\n--- Color Accuracy Analysis (Delta E) ---")
        
        # Convert the average sRGB color of the original image to CIELAB
        original_avg_srgb = sRGBColor(r_avg / 255, g_avg / 255, b_avg / 255)
        original_avg_lab = convert_color(original_avg_srgb, LabColor)

        # Define a perfect white reference in CIELAB (L=100, a=0, b=0)
        white_ref_lab = LabColor(lab_l=100.0, lab_a=0.0, lab_b=0.0)

        # Calculate the Delta E 2000 (dE00) value
        delta_e = delta_e_cie2000(original_avg_lab, white_ref_lab)

        print(f"Original image's average color: R:{r_avg:.2f}, G:{g_avg:.2f}, B:{b_avg:.2f}")
        print(f"Target white reference (CIELAB): L:{white_ref_lab.lab_l}, a:{white_ref_lab.lab_a}, b:{white_ref_lab.lab_b}")
        print(f"🎨 Delta E (CIEDE2000) of average color against white: {delta_e:.2f}")

        # Interpretation of Delta E values
        if delta_e <= 1.0:
            print("Conclusion: The color cast is not perceptible to the human eye. Excellent color accuracy.")
        elif delta_e <= 2.0:
            print("Conclusion: The color cast is perceptible with close observation. Very good color accuracy.")
        else:
            print("Conclusion: A significant color cast is present. Color accuracy is low.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found. Please ensure it is located at '{image_path}'.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the fixed image path
        image_file = get_qc_image_path()
        analyze_color_accuracy_and_white_balance(image_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")