#!/usr/bin/env python3
"""
PhotoQC Workflow Manager
Automates common development workflows and change management.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class PhotoQCWorkflow:
    def __init__(self):
        self.project_path = Path.cwd()
        self.git_available = self.check_git()
        
    def check_git(self):
        """Check if git is available and project is initialized"""
        try:
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def create_backup(self):
        """Create timestamped backup of all Python files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.project_path / f"backups/backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        python_files = list(self.project_path.glob("*.py"))
        for py_file in python_files:
            import shutil
            shutil.copy2(py_file, backup_dir / py_file.name)
        
        print(f"✅ Created backup in: {backup_dir}")
        return backup_dir
    
    def auto_commit_changes(self, message=None):
        """Automatically commit changes with meaningful message"""
        if not self.git_available:
            print("❌ Git not available or not initialized")
            return False
        
        # Check for changes
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if not result.stdout.strip():
            print("ℹ️  No changes to commit")
            return True
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Generate commit message if not provided
        if not message:
            # Analyze changes
            status_lines = result.stdout.strip().split('\n')
            modified_files = []
            new_files = []
            
            for line in status_lines:
                status = line[:2]
                filename = line[3:]
                if status.strip() == 'M':
                    modified_files.append(filename)
                elif status.strip() in ['A', '??']:
                    new_files.append(filename)
            
            parts = []
            if new_files:
                parts.append(f"Add {len(new_files)} new files")
            if modified_files:
                parts.append(f"Update {len(modified_files)} files")
            
            message = "Auto: " + ", ".join(parts) if parts else "Auto: Minor updates"
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            message += f" ({timestamp})"
        
        # Commit
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print(f"✅ Committed changes: {message}")
        return True
    
    def run_full_validation(self):
        """Run comprehensive validation suite"""
        print("🔍 Running full PhotoQC validation...")
        
        # Run auto validator
        try:
            result = subprocess.run([sys.executable, 'auto_validator.py'], 
                                  capture_output=True, text=True, check=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Validation failed:\n{e.stdout}\n{e.stderr}")
            return False
    
    def setup_development_environment(self):
        """One-time setup for optimal development environment"""
        print("🚀 Setting up PhotoQC development environment...")
        
        # Create necessary directories
        dirs = ['backups', 'output', 'logs', 'temp']
        for dir_name in dirs:
            (self.project_path / dir_name).mkdir(exist_ok=True)
        
        # Initialize git if not already done
        if not self.git_available:
            try:
                subprocess.run(['git', 'init'], check=True)
                print("✅ Initialized Git repository")
                self.git_available = True
            except:
                print("⚠️  Could not initialize Git repository")
        
        # Create initial commit if repository is empty
        if self.git_available:
            result = subprocess.run(['git', 'log', '--oneline'], 
                                  capture_output=True, text=True)
            if not result.stdout.strip():
                self.auto_commit_changes("Initial PhotoQC setup")
        
        print("✅ Development environment setup complete!")
    
    def quick_health_check(self):
        """Quick health check of the PhotoQC project"""
        print("🏥 PhotoQC Health Check")
        print("=" * 30)
        
        # Check essential files
        essential_files = ['image_utils.py', 'ImageQC.py', 'FullMetricList.py']
        for file in essential_files:
            if (self.project_path / file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ Missing: {file}")
        
        # Check QCImages folder
        qc_images = self.project_path / "QCImages"
        if qc_images.exists():
            image_files = list(qc_images.glob("*.{jpg,jpeg,png,tif,tiff}"))
            if image_files:
                print(f"✅ QCImages folder ({len(image_files)} images)")
            else:
                print("⚠️  QCImages folder empty")
        else:
            print("❌ Missing: QCImages folder")
        
        # Check for Python
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Python: {result.stdout.strip()}")
        except:
            print("❌ Python not available")

def main():
    workflow = PhotoQCWorkflow()
    
    if len(sys.argv) < 2:
        print("PhotoQC Workflow Manager")
        print("Usage:")
        print("  py workflow_manager.py setup     - Setup development environment")
        print("  py workflow_manager.py validate  - Run full validation")
        print("  py workflow_manager.py backup    - Create backup")
        print("  py workflow_manager.py commit    - Auto-commit changes")
        print("  py workflow_manager.py health    - Health check")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'setup':
        workflow.setup_development_environment()
    elif command == 'validate':
        workflow.run_full_validation()
    elif command == 'backup':
        workflow.create_backup()
    elif command == 'commit':
        message = sys.argv[2] if len(sys.argv) > 2 else None
        workflow.auto_commit_changes(message)
    elif command == 'health':
        workflow.quick_health_check()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()