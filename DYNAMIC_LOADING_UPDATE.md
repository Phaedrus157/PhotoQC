# Dynamic Image Loading - PhotoQC Update

## ✅ Update Complete!

All PhotoQC scripts have been successfully updated to use dynamic image loading. Here's what changed:

### 🔄 What Was Updated
- **27 Python scripts** now automatically detect images in the `QCImages` folder
- **No more hardcoded filenames** like "QCRef.jpg"
- **Flexible format support** - TIFF, PNG, JPEG automatically detected
- **Error handling** - Clear messages when no images are found

### 📁 Updated Scripts
All these scripts now work dynamically:
- `ImageQC.py` - Main image quality analysis
- `FullMetricList.py` - Comprehensive quality metrics
- `Brisque.py` - BRISQUE no-reference quality metric
- `BrennerQC.py` - Brenner sharpness metric
- `ImageSharpness.py` - Sharpness analysis suite
- Plus 20+ additional quality analysis scripts

### 🎯 How It Works Now

1. **Place any single image** in the `QCImages` folder
2. **Run any PhotoQC script** - it will automatically find your image
3. **Format priority**: TIFF > PNG > JPEG (for best quality analysis)
4. **Error handling**: Clear messages if no image is found

### 📝 Usage Examples

```bash
# Place your image in QCImages folder
# Example: QCImages/my_test_photo.tif

# Run any analysis script
py ImageQC.py
py FullMetricList.py  
py Brisque.py
# etc.
```

### ⚙️ Technical Details

- **New utility**: `image_utils.py` provides `get_qc_image_path()` function
- **Smart detection**: Finds first valid image in preferred format order
- **Robust error handling**: Helpful error messages for missing files/folders
- **Import injection**: All scripts now import the image utility function

### 🧪 Testing

To test the update:
1. Remove the placeholder file: `QCImages/PLACE_YOUR_IMAGE_HERE.txt`
2. Add a test image (TIFF, PNG, or JPEG) to the `QCImages` folder
3. Run: `py image_utils.py` to verify detection
4. Run any PhotoQC analysis script to confirm it works

### 🎉 Benefits

- **Flexible workflow** - No need to rename images to "QCRef.jpg"
- **Format consistency** - Prioritizes TIFF for best quality analysis  
- **Less error-prone** - No hardcoded paths to break
- **User-friendly** - Clear error messages guide usage
- **Maintainable** - Single utility function manages all image loading