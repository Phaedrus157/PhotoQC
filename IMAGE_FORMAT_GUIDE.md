# PhotoQC Image Format Guidelines

## Recommended Format: TIFF (.tif/.tiff)

### Why TIFF for Quality Control Analysis:
- **Lossless compression**: Preserves all image data for accurate metrics
- **16-bit depth support**: Better dynamic range and color accuracy analysis  
- **EXIF metadata**: Maintains camera settings needed for analysis
- **No compression artifacts**: Won't interfere with sharpness/noise detection
- **Professional standard**: Industry standard for image quality assessment

### Format Conversion Recommendations:
1. **From RAW (.orf, .raw)**: Export as 16-bit TIFF from your RAW processor
2. **From JPEG**: Only if no other option available (lossy compression affects results)
3. **Bit Depth**: Use 16-bit TIFF when possible for better dynamic range analysis

### File Naming Convention:
- Use descriptive names: `camera_model_iso_conditions.tif`
- Example: `pixel8_iso100_outdoor_daylight.tif`

### Current QC Image:
- Replace `QCImages/QCRef.jpg` with `QCImages/QCRef.tif`
- Ensures consistent, accurate quality measurements across all metrics

### Storage Considerations:
- TIFF files are larger than JPEG but smaller than uncompressed formats
- Use LZW compression in TIFF for space savings without quality loss