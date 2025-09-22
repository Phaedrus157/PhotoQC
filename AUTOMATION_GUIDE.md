# 🤖 PhotoQC Automation Configuration Guide

Your PhotoQC project is now equipped with comprehensive automation for efficient development and script management. Here's everything you need to know:

## 🚀 **Auto-Settings Overview**

### **VS Code Workspace Settings**
- **Auto-save**: Files save automatically when you switch focus
- **Format on save**: Python code auto-formats with Black (88 char lines)
- **Auto-import organization**: Imports are automatically organized and optimized
- **Smart linting**: Pylint configured for image processing libraries (OpenCV, NumPy, etc.)
- **Error detection**: Real-time syntax and import error highlighting
- **Image optimization**: Large image files excluded from file watching for performance

### **Automated Tasks (Ctrl+Shift+P → "Tasks: Run Task")**

#### **🏃‍♂️ Development Tasks**
- **🚀 Run Current Python File** - Execute currently open script
- **📦 Setup PhotoQC Dependencies** - Install all required packages
- **🔄 Auto-Format All Python Files** - Format entire project with Black
- **🧹 Clean Cache & Temp Files** - Remove __pycache__ and temp files

#### **🔬 Analysis Tasks**  
- **🔬 Run Full Image Quality Analysis** - Complete analysis suite
- **🎯 Run Basic Image QC** - Quick image quality check
- **📊 Run BRISQUE Quality Assessment** - No-reference quality metric
- **🔍 Run Sharpness Analysis** - Focus and sharpness evaluation

#### **🔧 Validation & Maintenance**
- **🔍 Validate All Scripts** - Comprehensive script validation
- **🏥 PhotoQC Health Check** - Project health assessment  
- **🚨 Check All Scripts for Errors** - Syntax error detection
- **💾 Create Project Backup** - Timestamped backup creation
- **📝 Auto-Commit Changes** - Intelligent Git commits
- **🚀 Setup Development Environment** - One-time environment setup

## 🛠️ **Automation Tools**

### **`auto_validator.py` - Script Validation**
Comprehensive validation of all PhotoQC scripts:
```bash
py auto_validator.py
```
**What it checks:**
- ✅ Python syntax errors
- ✅ Missing imports and dependencies  
- ✅ Image utility integration
- ✅ Old hardcoded file paths
- ✅ Best practices compliance

### **`workflow_manager.py` - Development Workflow**
Manages common development tasks:
```bash
py workflow_manager.py setup      # Setup dev environment
py workflow_manager.py validate   # Run full validation
py workflow_manager.py backup     # Create timestamped backup
py workflow_manager.py commit     # Auto-commit with smart messages
py workflow_manager.py health     # Quick health check
```

### **`image_utils.py` - Dynamic Image Loading**
Central utility for automatic image detection:
```bash
py image_utils.py  # Test image detection
```

## ⚙️ **Automatic Behaviors**

### **When You Edit Files:**
1. **Auto-save** when you switch between files
2. **Auto-format** Python code on save
3. **Auto-organize** imports
4. **Real-time** syntax checking
5. **Smart** error highlighting

### **When You Add Images:**
1. Scripts **automatically detect** any image in QCImages/
2. **Format priority**: TIFF → PNG → JPEG
3. **Clear error messages** if no images found
4. **Performance optimized** - large images excluded from file watching

### **When You Run Analysis:**
1. **Pre-validation** ensures image exists
2. **Dependency tasks** run automatically when needed
3. **Smart error handling** with helpful guidance
4. **Consistent output formatting**

## 🔄 **Workflow Integration**

### **Daily Development Workflow:**
1. **Open VS Code** in PhotoQC folder
2. **Add test image** to QCImages/ folder
3. **Run any analysis script** - it finds your image automatically
4. **Code gets auto-formatted** as you save
5. **Run validation** before major changes
6. **Auto-commit** when ready

### **Quality Assurance Workflow:**
1. **Health check** → `Ctrl+Shift+P` → "Tasks: Run Task" → "🏥 PhotoQC Health Check"
2. **Full validation** → "🔍 Validate All Scripts"
3. **Create backup** → "💾 Create Project Backup"
4. **Auto-commit** → "📝 Auto-Commit Changes"

## 📋 **Quick Reference**

### **VS Code Shortcuts:**
- `Ctrl+Shift+P` → "Tasks: Run Task" = Access all automation tasks
- `Ctrl+S` = Auto-save + auto-format current file
- `F5` = Run current Python file (if debug configured)
- `Ctrl+Shift+I` = Auto-format current file

### **Terminal Commands:**
```bash
# Core automation
py auto_validator.py                    # Validate all scripts
py workflow_manager.py health           # Quick health check
py image_utils.py                       # Test image detection

# Analysis (with any image in QCImages/)
py ImageQC.py                          # Basic quality analysis
py FullMetricList.py                   # Complete analysis suite
py Brisque.py                          # BRISQUE quality score

# Maintenance
py workflow_manager.py backup          # Create backup
py workflow_manager.py commit          # Auto-commit changes
py -m black . --line-length 88         # Format all files
```

## 🎯 **Customization**

### **Modify Settings:**
Edit `.vscode/settings.json` to customize:
- Auto-save timing
- Formatting preferences  
- Linting rules
- File associations

### **Add Tasks:**
Edit `.vscode/tasks.json` to add custom automation tasks

### **Extend Validation:**
Modify `auto_validator.py` to add custom validation rules

## 🚨 **Troubleshooting**

**Common Issues:**
- **Python not found**: Ensure `py` command works in terminal
- **Import errors**: Run dependency setup task
- **No images detected**: Check QCImages folder has valid image files
- **Git errors**: Initialize repository with `git init`

**Reset Everything:**
```bash
py workflow_manager.py setup  # Reinitialize environment
```

## 🎉 **Benefits**

✅ **Zero Configuration** - Works out of the box
✅ **Intelligent Automation** - Smart defaults for image processing
✅ **Error Prevention** - Validates before issues occur  
✅ **Consistent Quality** - Auto-formatting and linting
✅ **Flexible Workflow** - Adapts to any image you test
✅ **Professional Setup** - Industry best practices built-in

**Your PhotoQC project now runs like a well-oiled machine! 🔧✨**