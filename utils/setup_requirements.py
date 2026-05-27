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
    "pywt",                     # wavelet transforms (alias for PyWavelets)
    "piexif",                   # EXIF metadata
    "ipython",                  # Jupyter/Colab support
    "jupyter",                  # Jupyter notebooks
    "notebook",                 # Jupyter notebook server
    "seaborn",                  # optional: enhanced plotting
    "pandas",                   # optional: tabular data/logging
    "psd-tools"                 # PSD file creation and manipulation
]

# Aliases for packages with different PyPI names
package_aliases = {
    "pywt": "PyWavelets"
}

def install_packages(packages):
    for package in packages:
        actual_package = package_aliases.get(package, package)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", actual_package])
            print(f"✅ {package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}.")

def install_pyiqa():
    try:
        answer = input("metric_niqe.py requires pyiqa + PyTorch (~2GB). Install now? (y/n): ").strip().lower()
    except (EOFError, OSError):
        # Non-interactive environment — default to skip
        answer = "n"
    if answer == "y":
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyiqa", "--break-system-packages"])
            print("pyiqa installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install pyiqa.")
    else:
        print("Skipping pyiqa. metric_niqe.py will not run without it.")

if __name__ == "__main__":
    print("Installing required packages for ImageQC...")
    install_packages(required_packages)
    print("Package installation process completed.")
    print()
    install_pyiqa()
