import sys
import os
import cv2
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

# Import all your individual routine functions
from ImageFileAtrb import get_image_statistics
from ColorToneAnalysis import analyze_tonal_distribution
from NoiseAnalysis import analyze_noise
from ChromaticAberration import analyze_chromatic_aberration
from LensDistortion import analyze_lens_distortion
from Vignetting import analyze_vignetting
from CompressionArtifacts import analyze_compression_artifacts
from ImageSharpness import analyze_sharpness
from BrennerQC import calculate_brenner_sharpness
from CannyECS import count_canny_edges
# Corrected import for ColorfulMetric.py
from ColorfulMetric import calculate_colorfulness
from DynamRang import calculate_dynamic_range
from FFTSharp import fft_sharpness_score
from GabVarQC import gabor_variance
from GradMetric import gradient_metric
from LaplacianFilter import calculate_laplacian_metric
from LaplacianSharp import analyze_laplacian_sharpness
from LocalVar import local_variance_sharpness
from NoiseGrain import calculate_noise_metric
from NormAvGrad import normalized_average_gradient
from SobelEIS import sobel_eis_sharpness
from TenengradQC import tenengrad_focus_measure
from WaveSharp import wavelet_sharpness_score
from BlindDeconRL import run_blind_deconvolution

def run_all_analyses(image_path):
    """
    Executes all image quality analysis routines and prints a comprehensive report.
    This version relies on each individual script to handle its own output.
    """
    if not os.path.exists(image_path):
        print(f"❌ Error: The file '{image_path}' was not found.")
        return

    print("--- Starting Full Image Quality Analysis ---")

    # --- 1. Image File Attributes ---
    print("\n--- Image File Attributes ---")
    print("Running get_image_statistics...")
    get_image_statistics(image_path)

    # --- 2. Sharpness and Focus ---
    print("\n--- Sharpness and Focus ---")
    print("Running analyze_sharpness (Laplacian Variance)...")
    analyze_sharpness(image_path)
    
    print("\nRunning calculate_brenner_sharpness...")
    calculate_brenner_sharpness(image_path)
    
    print("\nRunning count_canny_edges...")
    count_canny_edges(image_path)

    print("\nRunning fft_sharpness_score...")
    fft_sharpness_score(image_path)
    
    print("\nRunning gabor_variance...")
    gabor_variance(image_path)
    
    print("\nRunning tenengrad_focus_measure...")
    tenengrad_focus_measure(image_path)
    
    print("\nRunning wavelet_sharpness_score...")
    wavelet_sharpness_score(image_path)
    
    print("\nRunning gradient_metric...")
    gradient_metric(image_path)
    
    print("\nRunning local_variance_sharpness...")
    local_variance_sharpness(image_path)
    
    print("\nRunning normalized_average_gradient...")
    normalized_average_gradient(image_path)
    
    print("\nRunning sobel_eis_sharpness...")
    sobel_eis_sharpness(image_path)
    
    print("\nRunning LaplacianFilter...")
    calculate_laplacian_metric(image_path)
    
    print("\nRunning LaplacianSharp...")
    analyze_laplacian_sharpness(image_path)
    
    # --- 3. Color and Tonal Analysis ---
    print("\n--- Color and Tonal Analysis ---")
    print("Running analyze_tonal_distribution...")
    analyze_tonal_distribution(image_path)
    
    print("\nRunning calculate_colorfulness...")
    calculate_colorfulness(image_path)
    
    print("\nRunning calculate_dynamic_range...")
    calculate_dynamic_range(image_path)

    # --- 4. Noise and Grain ---
    print("\n--- Noise and Grain ---")
    print("Running analyze_noise...")
    analyze_noise(image_path)
    
    print("\nRunning calculate_noise_metric...")
    calculate_noise_metric(image_path)

    print("\nRunning run_blind_deconvolution...")
    run_blind_deconvolution(image_path)

    # --- 5. Image Integrity and Artifacts ---
    print("\n--- Image Integrity and Artifacts ---")
    print("Running analyze_chromatic_aberration...")
    analyze_chromatic_aberration(image_path)
    
    print("\nRunning analyze_compression_artifacts...")
    analyze_compression_artifacts(image_path)
    
    # --- 6. Optical and Geometric Metrics ---
    print("\n--- Optical and Geometric Metrics ---")
    print("Running analyze_lens_distortion...")
    analyze_lens_distortion(image_path)
    
    print("\nRunning analyze_vignetting...")
    analyze_vignetting(image_path)

    print("\n--- Full Analysis Complete ---")

if __name__ == "__main__":
    image_file = os.path.join("QCImages", "QCRef.jpg")
    run_all_analyses(image_file)