#!/usr/bin/env python3
"""
PosterRend.py - Convert photographs to cartoon/comic book illustrations
Creates flat-colored cartoon style illustrations with bold outlines

Features:
- Posterization for flat color regions like cartoons/comics
- Bold black outlines for comic book style
- Color quantization for simplified palette
- Perfect for comic strip, animation, or cartoon-style graphics

Author: PhotoQC Project
Date: September 2025
"""

import cv2
import numpy as np
from PIL import Image
import os
import sys
from typing import Optional

# Import our dynamic image utility
try:
    from image_utils import get_qc_image_path
except ImportError:
    print("Error: image_utils.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

# Try to import PSD creation library
try:
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    PSD_AVAILABLE = True
except ImportError:
    PSD_AVAILABLE = False
    print("Warning: psd-tools not available. Will save as layered TIFF instead.")
    print("Install with: pip install psd-tools")

class PosterRenderer:
    """
    Advanced cartoon/comic book poster rendering engine
    """
    
    def __init__(self, image_path):
        """Initialize with image path"""
        self.image_path = image_path
        self.original_image: Optional[Image.Image] = None
        self.cv_image: Optional[np.ndarray] = None
        self.layers = {}
        
    def load_image(self):
        """Load and prepare the input image"""
        try:
            # Load with PIL for better color handling
            self.original_image = Image.open(self.image_path)
            if self.original_image.mode != 'RGB':
                self.original_image = self.original_image.convert('RGB')
            
            # Also load with OpenCV for edge detection
            self.cv_image = cv2.imread(self.image_path)
            if self.cv_image is None:
                raise ValueError(f"Could not load image: {self.image_path}")
            
            print(f"Loaded image: {self.image_path}")
            print(f"Size: {self.original_image.size}")
            return True
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def create_bold_outlines(self, line_thickness=3, blur_strength=7):
        """Create bold black outlines for comic book style"""
        if self.cv_image is None:
            raise ValueError("No image loaded. Call load_image() first.")
            
        # Convert to grayscale
        gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur to reduce noise while preserving edges
        gray_blur = cv2.medianBlur(gray, blur_strength)
        
        # Create adaptive threshold for bold outlines
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY, line_thickness*2+1, blur_strength)
        
        # Convert to 3-channel for blending
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        edges_pil = Image.fromarray(edges_colored)
        
        self.layers['bold_outlines'] = edges_pil
        return edges_pil
    
    def create_cartoon_colors(self, color_levels=8, blur_strength=15):
        """Create flat, posterized colors like cartoons/comics"""
        if self.original_image is None:
            raise ValueError("No image loaded. Call load_image() first.")
            
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)
        
        # Apply bilateral filter multiple times for cartoon effect
        # This smooths colors while preserving edges
        for _ in range(3):
            cv_image = cv2.bilateralFilter(cv_image, 9, 200, 200)
        
        # Convert to float for k-means clustering
        data = cv_image.reshape((-1, 3))
        data = np.float32(data)
        
        # Use k-means to reduce colors (posterize)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data, color_levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)  # type: ignore
        
        # Convert back to uint8 and reshape
        centers = np.uint8(centers)
        posterized_data = centers[labels.flatten()]  # type: ignore
        posterized_image = posterized_data.reshape(cv_image.shape)
        
        # Convert back to PIL RGB
        posterized_rgb = cv2.cvtColor(posterized_image, cv2.COLOR_BGR2RGB)
        cartoon_colors = Image.fromarray(posterized_rgb)
        
        self.layers['cartoon_colors'] = cartoon_colors
        return cartoon_colors
    
    def blend_cartoon_layers(self):
        """Blend layers to create final cartoon/comic book illustration"""
        if not self.layers:
            print("No layers created yet!")
            return None
        
        # Start with cartoon colors as the base
        if 'cartoon_colors' not in self.layers:
            print("Missing cartoon_colors layer!")
            return None
            
        result = self.layers['cartoon_colors'].copy()
        
        # Apply bold outlines with multiply blend for strong black lines
        if 'bold_outlines' in self.layers:
            result = self._multiply_blend(result, self.layers['bold_outlines'])
        
        self.layers['final_result'] = result
        return result
    
    def _multiply_blend(self, base, overlay):
        """Multiply blend mode for darkening effects"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        result_array = base_array * overlay_array
        result_array = (result_array * 255).astype(np.uint8)
        
        return Image.fromarray(result_array)
    
    def _overlay_blend(self, base, overlay, opacity=0.5):
        """Overlay blend mode with opacity control"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        # Overlay formula
        mask = base_array < 0.5
        result_array = np.where(mask, 
                               2 * base_array * overlay_array,
                               1 - 2 * (1 - base_array) * (1 - overlay_array))
        
        # Apply opacity
        result_array = base_array * (1 - opacity) + result_array * opacity
        result_array = np.clip(result_array * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result_array)
    
    def save_as_psd(self, output_path, include_layers=True):
        """Save the artwork as a PSD file with layers"""
        try:
            if not PSD_AVAILABLE:
                # Fallback to layered TIFF
                return self.save_as_layered_tiff(output_path.replace('.psd', '.tiff'))
            
            # Create PSD with layers
            from psd_tools import PSDImage
            from psd_tools.api.layers import PixelLayer
            
            # This is a simplified approach - for full PSD creation,
            # we'll use the photoshop-python library alternative
            print("Creating layered TIFF instead (full PSD creation requires Adobe SDK)")
            return self.save_as_layered_tiff(output_path.replace('.psd', '.tiff'))
            
        except Exception as e:
            print(f"Error saving PSD: {e}")
            print("Saving as regular PNG instead...")
            return self.save_as_png(output_path.replace('.psd', '.png'))
    
    def save_as_layered_tiff(self, output_path):
        """Save as layered TIFF (closest alternative to PSD)"""
        try:
            if 'final_result' not in self.layers:
                print("No final result to save!")
                return False
            
            # Save the final result
            final_image = self.layers['final_result']
            final_image.save(output_path, 'TIFF', save_all=True, compression='tiff_lzw')
            
            # Also save individual layers for manual PSD creation
            base_dir = os.path.dirname(output_path)
            base_name = os.path.splitext(os.path.basename(output_path))[0]
            
            layer_dir = os.path.join(base_dir, f"{base_name}_layers")
            os.makedirs(layer_dir, exist_ok=True)
            
            for layer_name, layer_image in self.layers.items():
                layer_path = os.path.join(layer_dir, f"{layer_name}.png")
                layer_image.save(layer_path, 'PNG')
            
            print(f"Saved layered illustration to: {output_path}")
            print(f"Individual layers saved to: {layer_dir}")
            return True
            
        except Exception as e:
            print(f"Error saving layered TIFF: {e}")
            return False
    
    def save_as_png(self, output_path):
        """Save as PNG (fallback option)"""
        try:
            if 'final_result' not in self.layers:
                print("No final result to save!")
                return False
            
            final_image = self.layers['final_result']
            final_image.save(output_path, 'PNG', optimize=True)
            
            print(f"Saved web illustration to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving PNG: {e}")
            return False
    
    def create_cartoon_illustration(self, 
                                   color_levels=6,
                                   line_thickness=7,
                                   blur_strength=7):
        """
        Complete cartoon/comic book illustration creation pipeline
        
        Args:
            color_levels (int): Number of color levels for posterization (4-12)
            line_thickness (int): Thickness of comic book outlines (3-9)  
            blur_strength (int): Smoothing strength for cartoon effect (5-15)
        """
        print("Starting cartoon illustration creation...")
        
        # Load the image
        if not self.load_image():
            return False
        
        # Create cartoon layers
        print("Creating flat cartoon colors...")
        self.create_cartoon_colors(color_levels=color_levels, blur_strength=blur_strength)
        
        print("Creating bold comic book outlines...")
        self.create_bold_outlines(line_thickness=line_thickness, blur_strength=blur_strength)
        
        # Blend layers for final cartoon effect
        print("Blending layers...")
        final_result = self.blend_cartoon_layers()
        
        if final_result:
            print("Cartoon illustration creation completed successfully!")
            return True
        else:
            print("Error creating cartoon illustration.")
            return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("PhotoQC PosterRend - Cartoon/Comic Illustration Generator")
    print("=" * 60)
    
    try:
        # Get the image path using our dynamic loading system
        image_path = get_qc_image_path()
        print(f"Processing image: {os.path.basename(image_path)}")
        
        # Create the poster renderer
        renderer = PosterRenderer(image_path)
        
        # Create the cartoon illustration with comic book parameters
        success = renderer.create_cartoon_illustration(
            color_levels=6,          # Flat color regions like comics
            line_thickness=7,        # Bold outlines like comic books
            blur_strength=7          # Smooth cartoon effect
        )
        
        if success:
            # Generate output filename - save to OneDrive Pictures folder
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_dir = r"C:\Users\jaa15\OneDrive\Pictures\APS images"
            os.makedirs(output_dir, exist_ok=True)
            
            # Try to save as PSD first, fallback to TIFF then PNG
            output_path = os.path.join(output_dir, f"{base_name}_cartoon_comic.psd")
            
            if renderer.save_as_psd(output_path):
                print(f"\n[SUCCESS] Cartoon comic illustration created successfully!")
                print(f"Output saved to: {output_path}")
            else:
                print("[ERROR] Error saving cartoon illustration file.")
                return False
            
            # Print layer information
            print(f"\nCreated layers:")
            for layer_name in renderer.layers.keys():
                print(f"  - {layer_name}")
            
            print(f"\n[COMPLETE] Cartoon comic processing complete!")
            
        else:
            print("[ERROR] Failed to create cartoon illustration.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()