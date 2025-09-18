import subprocess
import sys

# List of required packages
required_packages = [
    "opencv-python",            # cv2
    "numpy",                    # numerical operations
    "matplotlib",               # plotting
    "scipy",                    # FFT, filters
    "scikit-image",             # image metrics
    "Pillow",                   # image loading
    "piexif",                   # EXIF metadata
    "pywt",                     # wavelet transforms
    "ipython",                  # Jupyter/Colab support
    "jupyter",                  # Jupyter notebooks
    "notebook",                 # Jupyter notebook server
    "seaborn",                  # optional: enhanced plotting
    "pandas"                    # optional: tabular data/logging
]

def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    print("Installing required packages for ImageQC...")
    install_packages(required_packages)
    print("✅ All packages installed successfully.")
