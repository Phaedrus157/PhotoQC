#!/usr/bin/env python3
"""
PhotStration.py - Convert photographs to architectural illustration/map drawings
Creates detailed line drawings in the style of architectural maps and technical illustrations

Features:
- Fine line detection for architectural details
- Multiple edge detection techniques for building features
- Clean technical drawing aesthetic
- Map-like illustration rendering
- Preserves structural and architectural details
- Compatible with PhotoQC dynamic image loading system

Author: PhotoQC Project  
Date: September 2025
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os
import sys
from pathlib import Path

# Import our dynamic image utility
try:
    from image_utils import get_qc_image_path
except ImportError:
    print("Error: image_utils.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

class ArchitecturalRenderer:
    """
    Advanced architectural illustration and map drawing generator
    """
    
    def __init__(self, image_path):
        """Initialize with image path"""
        self.image_path = image_path
        self.original_image = None
        self.cv_image = None
        self.layers = {}
        
    def load_image(self):
        """Load and prepare the input image"""
        try:
            # Load with PIL for better color handling
            self.original_image = Image.open(self.image_path)
            if self.original_image.mode != 'RGB':
                self.original_image = self.original_image.convert('RGB')
            
            # Also load with OpenCV for advanced edge detection
            self.cv_image = cv2.imread(self.image_path)
            if self.cv_image is None:
                raise ValueError(f"Could not load image: {self.image_path}")
            
            print(f"Loaded image: {self.image_path}")
            print(f"Size: {self.original_image.size}")
            return True
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def create_fine_line_drawing(self, line_detail=1.0, edge_threshold=50):
        """Create fine detailed line work like architectural drawings"""
        # Convert to grayscale
        gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply slight blur to reduce noise but preserve details
        blurred = cv2.GaussianBlur(gray, (3, 3), 0.5)
        
        # Use Canny edge detection for fine lines
        edges = cv2.Canny(blurred, edge_threshold, edge_threshold * 2)
        
        # Enhance line detail with morphological operations
        if line_detail > 1.0:
            kernel = np.ones((2, 2), np.uint8)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Invert edges for black lines on white background
        edges = 255 - edges
        
        # Convert to RGB
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        fine_lines = Image.fromarray(edges_rgb)
        
        self.layers['fine_lines'] = fine_lines
        return fine_lines
    
    def create_structural_details(self, detail_threshold=100):
        """Create structural and architectural detail lines"""
        # Convert to grayscale
        gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive threshold for structural details
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Detect strong structural lines using Hough transforms
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=detail_threshold)
        
        # Create image for drawing lines
        line_img = np.ones_like(gray) * 255
        
        if lines is not None:
            for line in lines[0:200]:  # Limit to strongest lines
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                
                cv2.line(line_img, (x1, y1), (x2, y2), 0, 1)
        
        # Combine with adaptive threshold
        structural = cv2.bitwise_and(line_img.astype(np.uint8), adaptive_thresh)
        
        # Convert to RGB
        structural_rgb = cv2.cvtColor(structural, cv2.COLOR_GRAY2RGB)
        structural_details = Image.fromarray(structural_rgb)
        
        self.layers['structural_details'] = structural_details
        return structural_details
    
    def create_depth_contours(self, contour_levels=5):
        """Create contour-like depth lines for architectural depth"""
        # Convert to grayscale
        gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur for smooth contours
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Create contour-like lines at different intensity levels
        contour_img = np.ones_like(gray) * 255
        
        for level in range(contour_levels):
            threshold_val = int(255 / contour_levels * (level + 1))
            _, thresh = cv2.threshold(blurred, threshold_val, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw contours
            cv2.drawContours(contour_img, contours, -1, 0, 1)
        
        # Convert to RGB
        contour_rgb = cv2.cvtColor(contour_img, cv2.COLOR_GRAY2RGB)
        depth_contours = Image.fromarray(contour_rgb)
        
        self.layers['depth_contours'] = depth_contours
        return depth_contours
    
    def create_hatching_texture(self, hatch_density=0.3):
        """Create architectural hatching/crosshatching for shading"""
        # Convert to grayscale for shadow analysis
        gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        
        # Create shadow mask (darker areas need hatching)
        _, shadow_mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Create hatching pattern
        height, width = gray.shape
        hatch_img = np.ones((height, width), dtype=np.uint8) * 255
        
        # Add diagonal hatching lines
        spacing = int(10 / hatch_density)  # Adjust line spacing based on density
        
        # Diagonal lines (\)
        for i in range(0, height + width, spacing):
            cv2.line(hatch_img, (0, i), (i, 0), 0, 1)
        
        # Cross-hatching (/)
        for i in range(-width, height, spacing):
            cv2.line(hatch_img, (0, height - i), (width + i, 0), 0, 1)
        
        # Apply hatching only to shadow areas
        hatched = cv2.bitwise_or(hatch_img, shadow_mask)
        
        # Convert to RGB
        hatched_rgb = cv2.cvtColor(hatched, cv2.COLOR_GRAY2RGB)
        hatching = Image.fromarray(hatched_rgb)
        
        self.layers['hatching_texture'] = hatching
        return hatching
    
    def blend_architectural_layers(self):
        """Blend all layers to create final architectural illustration"""
        if not self.layers:
            print("No layers created yet!")
            return None
        
        # Start with white background
        if 'fine_lines' not in self.layers:
            print("Missing fine_lines layer!")
            return None
            
        # Create base white image
        width, height = self.original_image.size
        result = Image.new('RGB', (width, height), 'white')
        
        # Apply fine lines (primary detail)
        if 'fine_lines' in self.layers:
            result = self._multiply_blend(result, self.layers['fine_lines'])
        
        # Add structural details
        if 'structural_details' in self.layers:
            result = self._multiply_blend(result, self.layers['structural_details'])
        
        # Add depth contours (lighter blend)
        if 'depth_contours' in self.layers:
            result = Image.blend(result, self.layers['depth_contours'], 0.3)
        
        # Add hatching texture (very light)
        if 'hatching_texture' in self.layers:
            result = Image.blend(result, self.layers['hatching_texture'], 0.2)
        
        self.layers['final_result'] = result
        return result
    
    def _multiply_blend(self, base, overlay):
        """Multiply blend mode for darkening line effects"""
        base_array = np.array(base, dtype=np.float32) / 255.0
        overlay_array = np.array(overlay, dtype=np.float32) / 255.0
        
        result_array = base_array * overlay_array
        result_array = (result_array * 255).astype(np.uint8)
        
        return Image.fromarray(result_array)
    
    def save_as_png(self, output_path):
        """Save architectural illustration as PNG"""
        try:
            if 'final_result' not in self.layers:
                print("No final result to save!")
                return False
            
            final_image = self.layers['final_result']
            final_image.save(output_path, 'PNG', optimize=True)
            
            print(f"Saved architectural illustration to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving PNG: {e}")
            return False
    
    def save_as_layered_tiff(self, output_path):
        """Save as layered TIFF with individual layers"""
        try:
            if 'final_result' not in self.layers:
                print("No final result to save!")
                return False
            
            # Save the final result
            final_image = self.layers['final_result']
            final_image.save(output_path, 'TIFF', save_all=True, compression='tiff_lzw')
            
            # Also save individual layers
            base_dir = os.path.dirname(output_path)
            base_name = os.path.splitext(os.path.basename(output_path))[0]
            
            layer_dir = os.path.join(base_dir, f"{base_name}_layers")
            os.makedirs(layer_dir, exist_ok=True)
            
            for layer_name, layer_image in self.layers.items():
                layer_path = os.path.join(layer_dir, f"{layer_name}.png")
                layer_image.save(layer_path, 'PNG')
            
            print(f"Saved architectural illustration to: {output_path}")
            print(f"Individual layers saved to: {layer_dir}")
            return True
            
        except Exception as e:
            print(f"Error saving layered TIFF: {e}")
            return False
    
    def create_architectural_illustration(self, 
                                        line_detail=1.2,
                                        edge_threshold=40,
                                        detail_threshold=80,
                                        contour_levels=4,
                                        hatch_density=0.2):
        """
        Complete architectural illustration creation pipeline
        
        Args:
            line_detail (float): Fine line detail level (0.5-2.0)
            edge_threshold (int): Edge detection sensitivity (20-100)
            detail_threshold (int): Structural detail threshold (50-150)
            contour_levels (int): Number of depth contour levels (3-8)
            hatch_density (float): Hatching texture density (0.1-0.5)
        """
        print("Starting architectural illustration creation...")
        
        # Load the image
        if not self.load_image():
            return False
        
        # Create architectural layers
        print("Creating fine line drawing...")
        self.create_fine_line_drawing(line_detail=line_detail, edge_threshold=edge_threshold)
        
        print("Creating structural details...")
        self.create_structural_details(detail_threshold=detail_threshold)
        
        print("Creating depth contours...")
        self.create_depth_contours(contour_levels=contour_levels)
        
        print("Creating hatching texture...")
        self.create_hatching_texture(hatch_density=hatch_density)
        
        # Blend all layers
        print("Blending architectural layers...")
        final_result = self.blend_architectural_layers()
        
        if final_result:
            print("Architectural illustration creation completed successfully!")
            return True
        else:
            print("Error creating architectural illustration.")
            return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("PhotoQC PhotStration - Architectural Illustration Generator")
    print("=" * 60)
    
    try:
        # Get the image path using our dynamic loading system
        image_path = get_qc_image_path()
        print(f"Processing image: {os.path.basename(image_path)}")
        
        # Create the architectural renderer
        renderer = ArchitecturalRenderer(image_path)
        
        # Create the architectural illustration
        success = renderer.create_architectural_illustration(
            line_detail=1.2,         # Fine detailed lines
            edge_threshold=40,       # Sensitive edge detection
            detail_threshold=80,     # Moderate structural detail
            contour_levels=4,        # Depth contours
            hatch_density=0.2        # Light hatching texture
        )
        
        if success:
            # Generate output filename - save to OneDrive Pictures folder
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_dir = r"C:\Users\jaa15\OneDrive\Pictures\APS images"
            os.makedirs(output_dir, exist_ok=True)
            
            # Save as both TIFF and PNG
            tiff_path = os.path.join(output_dir, f"{base_name}_architectural_map.tiff")
            png_path = os.path.join(output_dir, f"{base_name}_architectural_map.png")
            
            # Save layered TIFF
            if renderer.save_as_layered_tiff(tiff_path):
                print(f"\n[SUCCESS] Architectural illustration created successfully!")
                print(f"Layered TIFF saved to: {tiff_path}")
            
            # Also save PNG for easy viewing
            if renderer.save_as_png(png_path):
                print(f"PNG version saved to: {png_path}")
            
            # Print layer information
            print(f"\nCreated layers:")
            for layer_name in renderer.layers.keys():
                print(f"  - {layer_name}")
            
            print(f"\n[COMPLETE] Architectural illustration processing complete!")
            
        else:
            print("[ERROR] Failed to create architectural illustration.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()