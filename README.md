# 📷 PhotoQC

Python scripts for quantitative image quality analysis prior to stock photo submission. Each script is standalone and accepts image paths as arguments.

## Structure

### metric/
Single-metric scripts — each measures one specific quality attribute.

| Script | Metric |
|---|---|
| metric_laplacian.py | Laplacian variance sharpness (with stock threshold interpretation) |
| metric_laplacian_smoothed.py | Laplacian variance with Gaussian pre-smoothing |
| metric_brenner.py | Brenner gradient sharpness |
| metric_canny.py | Canny edge count sharpness proxy |
| metric_tenengrad.py | Tenengrad focus measure |
| metric_sobel.py | Sobel edge intensity sum |
| metric_gabor.py | Gabor filter variance sharpness |
| metric_fft.py | FFT high-frequency energy ratio |
| metric_wavelet.py | Wavelet DWT high-frequency energy sharpness |
| metric_localvar.py | Sliding-window local variance sharpness |
| metric_normgrad.py | Normalized average gradient |
| metric_blinddecon.py | Richardson-Lucy blur estimation |
| metric_colorfulness.py | Hasler-Suesstrunk colorfulness score |
| metric_colorcast.py | RGB color cast detection |
| metric_coloraccuracy.py | Gray-world white balance + Delta-E color accuracy |
| metric_toneanalysis.py | Luminance histogram shadow/highlight clipping |
| metric_gradentropy.py | Histogram entropy as tonal graduation quality |
| metric_noise.py | Laplacian + YCbCr channel noise analysis |
| metric_brisque.py | BRISQUE blind perceptual quality score |
| metric_niqe.py | NIQE no-reference quality score (requires pyiqa + PyTorch) |
| metric_chromatic.py | Chromatic aberration channel shift score |
| metric_lensdistortion.py | Barrel/pincushion lens distortion via Hough lines |
| metric_vignetting.py | Center-to-corner brightness falloff score |
| metric_compression.py | JPEG blocking artifact detection |
| metric_jpegquality.py | JPEG quantization table quality estimate |

### suite/
Multi-metric scripts — each runs several related metrics in a single pass.

| Script | Metrics combined |
|---|---|
| suite_sharpness_reference.py | Laplacian, Brenner, Tenengrad, Gabor (ref vs test comparison) |
| suite_ssim_psnr.py | SSIM + PSNR full-reference comparison |
| suite_dynrange.py | Luminance std dev + pixel intensity range |
| suite_color.py | Colorfulness, tonal distribution, color accuracy |
| suite_tif_vs_dng.py | 8-metric comparison of two image files (any format) |
| suite_paired_compare.py | 5-metric averaged comparison across two matched image folders |

### utils/
| Script | Role |
|---|---|
| image_utils.py | QC image path resolver |
| image_file_attributes.py | Image dimensions, EXIF metadata reporter |
| gaussian_smooth.py | Gaussian blur preprocessing helper |
| setup_requirements.py | pip installer for all dependencies |
| auto_validator.py | AST syntax and import checker for all repo scripts |

## Usage

All scripts accept image paths as arguments:

```bash
# Single-metric
py metric/metric_laplacian.py <image_path>
py metric/metric_tenengrad.py <image_path>
py metric/metric_fft.py <image_path>

# Multi-metric suites
py suite/suite_dynrange.py <image_path>
py suite/suite_color.py <image_path>
py suite/suite_tif_vs_dng.py <ref_path> <compare_path>
py suite/suite_paired_compare.py <folder1> <folder2>
py suite/suite_sharpness_reference.py <reference_image> <test_image>

# Utils
py utils/gaussian_smooth.py <input_image> <output_image>
```

## Input Folder

Place test images in: `C:\TEMP\QCImages\`
Supported formats: TIFF, PNG, JPEG (TIFF preferred)

All `metric/` and `suite/` scripts scan this folder automatically — no CLI arguments required.

For suite scripts comparing two images (`suite_paired_compare`, `suite_sharpness_reference`, `suite_ssim_psnr`, `suite_tif_vs_dng`), place exactly two images in the folder. Scripts pick the first two files found by extension priority: `tif > tiff > png > jpg > jpeg`.

The `QCImages/` folder in the project root is for documentation only — do not place test images there.

## Dependencies

Standard install (`pip install -r requirements.txt` or via `setup_requirements.py`):
- `opencv-python`, `numpy`, `scipy`, `scikit-image`, `Pillow`, `matplotlib`, `colormath`, `brisque`

Heavy optional dependency (required for `metric_niqe.py` only):
- `pyiqa` + PyTorch (~2GB install)
- Install with: `pip install pyiqa --break-system-packages`
- On first run, `metric_niqe.py` will download a small model file (~8KB) from HuggingFace

## Output

Metric scripts print scores to stdout. Suite scripts additionally write timestamped logs to:

```
C:\Users\Public\Documents\PYProjects\Logs\
```

## Logs

Suite scripts that generate logs write to: `C:\Users\Public\Documents\PYProjects\Logs\`
