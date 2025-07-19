# MIT License
#
# Copyright (c) 2025 Florian Lorenzen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Common build configuration for Friesen Enrollment Converter
"""
import os
import sys
from pathlib import Path

# Project information
PROJECT_NAME = "friesen-enrollment-conversion"
APP_NAME = "Friesen Enrollment Converter"
VERSION = "0.0.1-dev"  # Default version for local development
AUTHOR = "Florian Lorenzen"
DESCRIPTION = "Friesen Enrollment Converter - Convert and process enrollment files"

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
MAIN_SCRIPT = SRC_DIR / "main.py"
DIST_DIR = PROJECT_ROOT / "dist"
WORK_DIR = PROJECT_ROOT / "build" / "temp"

# Common PyInstaller settings
COMMON_PYINSTALLER_OPTIONS = {
    "clean": True,
    "noconfirm": True,
    "collect_all": ["openpyxl", "pypdf", "reportlab", "customtkinter"],
}

# Common hidden imports
COMMON_HIDDEN_IMPORTS = [
    "customtkinter",
    "tkinter",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "PIL",
    "PIL._tkinter_finder",
    # Our custom modules
    "converter",
    "src.converter",
    # PDF conversion dependencies
    "openpyxl",
    "openpyxl.workbook",
    "openpyxl.worksheet",
    "openpyxl.cell",
    "pypdf",
    "pypdf._reader",
    "pypdf._writer",
    "reportlab",
    "reportlab.pdfgen",
    "reportlab.pdfgen.canvas",
    "reportlab.lib.colors",
    "reportlab.lib.pagesizes",
    "reportlab.lib.styles",
    "reportlab.platypus",
    # Additional dependencies that might be needed
    "et_xmlfile",
    "packaging",
    "darkdetect",
]

# Files to exclude to reduce size
COMMON_EXCLUDES = [
    "matplotlib",
    "numpy",
    "scipy",
    "jupyter",
    "IPython",
    "notebook",
    "pytest",
    # Don't exclude setuptools/pip as they might be needed by dependencies
]

def get_common_data_files():
    """Get list of common data files to include, checking if they exist"""
    data_files = []
    
    # Include the PDF form template if it exists
    form_pdf = PROJECT_ROOT / "resources" / "form.pdf"
    if form_pdf.exists():
        data_files.append((str(form_pdf), "resources"))
    
    return data_files

COMMON_DATA_FILES = get_common_data_files()

def get_version_info(version=None):
    """Return version info for executables"""
    if version is None:
        version = VERSION
    
    # Convert version string to tuple for version info
    # Handle semantic versioning (e.g., "1.2.3" -> (1, 2, 3, 0))
    # Handle development versions (e.g., "1.2.3-dev" -> (1, 2, 3, 0))
    version_parts = version.split('.')
    if len(version_parts) >= 3:
        # Handle patch version that might contain a dash (e.g., "1-dev")
        patch_part = version_parts[2]
        if '-' in patch_part:
            patch_part = patch_part.split('-')[0]
        
        try:
            major = int(version_parts[0])
            minor = int(version_parts[1])
            patch = int(patch_part)
            build = 0
        except ValueError:
            # Fallback for malformed versions
            major, minor, patch, build = 1, 0, 0, 0
    else:
        major, minor, patch, build = 1, 0, 0, 0
    
    return {
        'major': major,
        'minor': minor,
        'patch': patch,
        'build': build,
        'version': version
    }

def validate_environment():
    """Common environment validation"""
    print("Validating build environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8+ required")
    
    # Check if main script exists
    if not MAIN_SCRIPT.exists():
        raise RuntimeError(f"Main script not found: {MAIN_SCRIPT}")
    
    # Check if we're in the right directory
    if not (PROJECT_ROOT / "src").exists():
        raise RuntimeError("Please run this script from the project root directory")
    
    # Check if runtime dependencies are installed
    runtime_deps = ["openpyxl", "pypdf", "reportlab", "customtkinter"]
    missing_deps = []
    
    for dep in runtime_deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print("ERROR: Missing runtime dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nPlease install runtime dependencies first:")
        print("   pip install -r requirements.txt")
        print("\nThen run the build again.")
        raise RuntimeError("Runtime dependencies not installed")
    
    print("OK: Runtime dependencies found")
    
    # Test converter import specifically
    try:
        # Add src to path temporarily
        original_path = sys.path.copy()
        sys.path.insert(0, str(PROJECT_ROOT / "src"))
        from converter import Converter, ConversionError
        sys.path = original_path  # Restore original path
        print("OK: Converter module import successful")
    except ImportError as e:
        print(f"ERROR: Converter module import failed: {e}")
        print("This might cause issues in the bundled executable.")
    
    # Check if form.pdf exists (optional)
    form_pdf = PROJECT_ROOT / "resources" / "form.pdf"
    if form_pdf.exists():
        print("OK: Form template found")
    else:
        print("INFO: Form template not found (optional) - basic forms will be generated")
    
    print("OK: Environment validation passed")

def clean_build_directories(build_dir, dist_dir, work_dir):
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    dirs_to_clean = [dist_dir, work_dir, PROJECT_ROOT / "build" / "temp"]
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"   Removed: {dir_path}")
    
    print("OK: Build directories cleaned")

def install_build_dependencies(requirements_file):
    """Install build dependencies"""
    print("Installing build dependencies...")
    
    if not requirements_file.exists():
        raise RuntimeError(f"Build requirements file not found: {requirements_file}")
    
    try:
        import subprocess
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file),
            "--only-binary=all", "--upgrade"
        ], check=True, capture_output=True, text=True)
        print("OK: Build dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e.stderr}")
        raise RuntimeError("Dependency installation failed") 