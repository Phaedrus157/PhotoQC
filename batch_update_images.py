#!/usr/bin/env python3
"""
Batch update script to replace hardcoded image paths with dynamic image loading
across all PhotoQC scripts.
"""

import os
import re

# List of files that need updating based on our grep search
files_to_update = [
    "ColorAnalysisFull.py",
    "ColorAccuracy.py", 
    "ChromaticAberration.py",
    "BUFullMetric.py",
    "ColorCastDet.py",
    "ColorToneAnalysis.py",
    "CompressionArtifacts.py",
    "BlindDeconRL.py",
    "findpic.py",
    "FullRefMetric.py", 
    "GSmooth.py",
    "ImageFileAtrb.py",
    "JPEGCompQE.py",
    "LaPlVarGausmth.py",
    "LensDistortion.py",
    "LocalVar.py",
    "niqe.py",
    "NoiseAnalysis.py",
    "SSIMPSNR.py",
    "Vignetting.py"
]

def update_file(filepath):
    """Update a single file to use dynamic image loading"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    print(f"Updating {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import if not already present
        if 'from image_utils import get_qc_image_path' not in content:
            # Find existing imports and add after them
            lines = content.split('\n')
            import_inserted = False
            new_lines = []
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                # Insert after other imports
                if (line.startswith('import ') or line.startswith('from ')) and not import_inserted:
                    # Look ahead to see if there are more imports
                    has_more_imports = False
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].startswith('import ') or lines[j].startswith('from '):
                            has_more_imports = True
                            break
                    if not has_more_imports:
                        new_lines.append('from image_utils import get_qc_image_path')
                        import_inserted = True
            
            content = '\n'.join(new_lines)
        
        # Replace hardcoded image paths with dynamic loading
        patterns = [
            # Pattern 1: image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")
            (r'image_file\s*=\s*os\.path\.join\(os\.getcwd\(\),\s*["\']QCImages["\']\s*,\s*["\']QCRef\.jpg["\']\)',
             'image_file = get_qc_image_path()'),
            
            # Pattern 2: image_file = "QCImages/QCRef.jpg" 
            (r'image_file\s*=\s*["\']QCImages/QCRef\.jpg["\']',
             'image_file = get_qc_image_path()'),
            
            # Pattern 3: image_path = "QCImages/QCRef.jpg"
            (r'image_path\s*=\s*["\']QCImages/QCRef\.jpg["\']',
             'image_path = get_qc_image_path()'),
            
            # Pattern 4: file_name = "QCRef.jpg" (when used with QCImages)
            (r'file_name\s*=\s*["\']QCRef\.jpg["\']',
             'image_path = get_qc_image_path()'),
            
            # Pattern 5: img_path = "/workspaces/PhotoQC/QCImages/QCRef.jpg"
            (r'img_path\s*=\s*["\'][^"\']*QCImages[^"\']*QCRef\.jpg["\']',
             'img_path = get_qc_image_path()'),
            
            # Pattern 6: image_path = os.path.join("QCImages", "QCRef2.jpg")
            (r'image_path\s*=\s*os\.path\.join\(["\']QCImages["\']\s*,\s*["\']QCRef2\.jpg["\']\)',
             'image_path = get_qc_image_path()'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Add error handling to main sections
        if 'if __name__ == "__main__"' in content:
            # Replace simple main sections with try-except blocks
            main_pattern = r'if __name__ == "__main__":\s*\n((?:\s{4}.*\n?)*)'
            
            def replace_main(match):
                main_content = match.group(1)
                # Don't wrap if already has try-except
                if 'try:' in main_content and 'except' in main_content:
                    return match.group(0)
                
                # Add try-except wrapper
                indented_content = '\n'.join(['    ' + line if line.strip() else line 
                                            for line in main_content.split('\n')])
                
                return f'''if __name__ == "__main__":
    try:
{indented_content}    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {{e}}")
        print("Please place a valid image file (TIFF, PNG, or JPEG) in the QCImages folder.")'''
            
            content = re.sub(main_pattern, replace_main, content, flags=re.MULTILINE)
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all files"""
    print("🔄 Starting batch update of PhotoQC scripts...")
    print("=" * 50)
    
    updated_count = 0
    total_count = 0
    
    for filename in files_to_update:
        filepath = os.path.join(os.getcwd(), filename)
        total_count += 1
        if update_file(filepath):
            updated_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 Update Summary: {updated_count}/{total_count} files successfully updated")
    print("🎉 Batch update completed!")

if __name__ == "__main__":
    main()