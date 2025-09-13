import cv2
import os
import sys
import piexif
from PIL import Image

def get_image_statistics(image_path):
    """
    Retrieves and prints a comprehensive set of image statistics,
    including an estimation of the original camera's megapixel count.

    Parameters:
        image_path (str): The path to the image file.
    """
    # Check if the file exists first
    if not os.path.exists(image_path):
        sys.stdout.write(f"Error: The image file was not found at {image_path}\n")
        sys.exit(1) # Exit cleanly with an error code

    # Open image with OpenCV for dimensions and with PIL for other attributes
    cv2_image = cv2.imread(image_path)
    if cv2_image is None:
        sys.stdout.write("Error: Could not load the image with OpenCV. Check file integrity or format.\n")
        sys.exit(1)
        
    try:
        pil_image = Image.open(image_path)
    except IOError as e:
        sys.stdout.write(f"Error: Could not open the image with Pillow. {e}\n")
        sys.exit(1)
        
    # Get basic image attributes
    width, height = pil_image.size
    megapixels = (width * height) / 1000000.0

    # Determine the original MP rating and apply the "HR" label if applicable
    original_mp_label = "N/A"
    if megapixels > 75 and megapixels < 85:
        original_mp_label = "80MP HR"
    elif megapixels > 45 and megapixels < 55:
        original_mp_label = "50MP HR"
    elif megapixels > 15 and megapixels < 25:
        original_mp_label = "20MP"
    else:
        original_mp_label = "Other"

    file_size_kb = os.path.getsize(image_path) / 1024.0
    
    # Get color space and bit depth
    color_space = pil_image.mode
    if 'L' in color_space:
        bit_depth = 8 # Grayscale
    elif 'RGB' in color_space:
        bit_depth = 24 # 8 bits per channel
    else:
        bit_depth = "unknown"

    # Get EXIF data
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
        
    # Print the output in a single column
    sys.stdout.write(f"filenames = {os.path.basename(image_path)}\n")
    sys.stdout.write(f"pixel dimensions = {width}x{height}\n")
    sys.stdout.write(f"original MP = {original_mp_label}\n")
    sys.stdout.write(f"filesizeKB = {file_size_kb:.2f}\n")
    sys.stdout.write(f"filesizeMP = {megapixels:.2f}\n")
    sys.stdout.write(f"bit depth = {bit_depth} bits\n")
    sys.stdout.write(f"color space = {color_space}\n")
    sys.stdout.write(f"camera model = {camera_model}\n")
    sys.stdout.write(f"exposure time = {exposure_time}\n")
    sys.stdout.write(f"ISO = {iso}\n")

# --- Main part of the script ---
if __name__ == "__main__":
    folder_name = "QCImages"
    file_name = "QCRef2.jpg"
    image_path = os.path.join(folder_name, file_name)
    
    get_image_statistics(image_path)
