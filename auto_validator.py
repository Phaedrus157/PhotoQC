#!/usr/bin/env python3
"""
PhotoQC Auto-Validator
Automatically validates all PhotoQC scripts for import issues, syntax errors, and compatibility.
"""

import os
import sys
import ast
import subprocess
import importlib.util
from pathlib import Path

class PhotoQCValidator:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.python_files = list(self.project_path.glob("*.py"))
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def validate_syntax(self, file_path):
        """Check Python syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Parse error: {e}"
    
    def validate_imports(self, file_path):
        """Check if all imports are available"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            missing = []
            for imp in imports:
                try:
                    if imp == "image_utils":
                        # Special case for our utility
                        if not (self.project_path / "image_utils.py").exists():
                            missing.append(imp)
                    else:
                        importlib.import_module(imp.split('.')[0])
                except ImportError:
                    missing.append(imp)
            
            return len(missing) == 0, missing
            
        except Exception as e:
            return False, [f"Import check failed: {e}"]
    
    def check_image_utils_integration(self, file_path):
        """Check if script properly uses image_utils"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip utility files and setup files
            if file_path.name in ['image_utils.py', 'SetUpReqs.py', 'batch_update_images.py']:
                return True, "Utility file - skip check"
            
            # Check for old hardcoded paths
            old_patterns = ['QCRef.jpg', 'QCRef2.jpg', 'QCRef_GT.jpg']
            found_old = [p for p in old_patterns if p in content]
            
            if found_old:
                return False, f"Old hardcoded paths found: {found_old}"
            
            # Check for image_utils import
            if 'from image_utils import' in content or 'import image_utils' in content:
                return True, "Uses dynamic image loading"
            else:
                # Check if it's a script that should use image loading
                if any(pattern in content for pattern in ['cv2.imread', 'Image.open', 'image_path']):
                    return False, "Should use image_utils for image loading"
                return True, "No image loading detected"
            
        except Exception as e:
            return False, f"Integration check failed: {e}"
    
    def run_validation(self):
        """Run full validation suite"""
        print("🔍 PhotoQC Auto-Validator Starting...")
        print("=" * 50)
        
        for py_file in self.python_files:
            print(f"\n📄 Validating {py_file.name}...")
            
            # Syntax check
            syntax_ok, syntax_error = self.validate_syntax(py_file)
            if not syntax_ok:
                self.errors.append(f"{py_file.name}: {syntax_error}")
                print(f"  ❌ Syntax: {syntax_error}")
                continue
            else:
                print("  ✅ Syntax: OK")
            
            # Import check
            imports_ok, missing_imports = self.validate_imports(py_file)
            if not imports_ok:
                self.warnings.append(f"{py_file.name}: Missing imports: {missing_imports}")
                print(f"  ⚠️  Imports: Missing {missing_imports}")
            else:
                print("  ✅ Imports: OK")
            
            # Image utils integration check
            integration_ok, integration_msg = self.check_image_utils_integration(py_file)
            if not integration_ok:
                self.warnings.append(f"{py_file.name}: {integration_msg}")
                print(f"  ⚠️  Integration: {integration_msg}")
            else:
                print(f"  ✅ Integration: {integration_msg}")
            
            if syntax_ok and imports_ok and integration_ok:
                self.success_count += 1
        
        self.print_summary()
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 50)
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully validated: {self.success_count}/{len(self.python_files)} files")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n🎉 All files passed validation!")
        
        print("\n💡 Tip: Run 'py -m py_compile filename.py' to test individual files")

if __name__ == "__main__":
    validator = PhotoQCValidator()
    validator.run_validation()