import subprocess
import sys

# Expanded list of required packages for ImageQC
required_packages = [
    "opencv-python",            # cv2 for image processing
    # "opencv-contrib-python",  # additional OpenCV modules (commented due to install issue)
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
    "seaborn",                  # enhanced plotting
    "pandas",                   # tabular data/logging
    "imageio",                  # flexible image I/O
    "tqdm",                     # progress bars
    "pyyaml",                   # config file support
    "loguru"                    # advanced logging
]

def install_packages(packages):
    for package in packages:
        print(f"📦 Installing: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("✅ All packages installed successfully.")

if __name__ == "__main__":
    print("🔧 Starting installation of required packages for ImageQC...")
    install_packages(required_packages)
