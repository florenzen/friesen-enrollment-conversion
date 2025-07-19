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
Build configuration for macOS app bundle
"""
import sys
from pathlib import Path

# Add the common directory to the path
common_dir = Path(__file__).parent.parent / "common"
if str(common_dir) not in sys.path:
    sys.path.insert(0, str(common_dir))

# Import common configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
import build_config as common_config

# Re-export common variables for easier access
PROJECT_ROOT = common_config.PROJECT_ROOT
APP_NAME = common_config.APP_NAME
VERSION = common_config.VERSION
AUTHOR = common_config.AUTHOR
DESCRIPTION = common_config.DESCRIPTION
MAIN_SCRIPT = common_config.MAIN_SCRIPT
COMMON_HIDDEN_IMPORTS = common_config.COMMON_HIDDEN_IMPORTS
COMMON_EXCLUDES = common_config.COMMON_EXCLUDES

# macOS-specific paths
BUILD_DIR = common_config.PROJECT_ROOT / "build" / "macos"
DIST_DIR = common_config.PROJECT_ROOT / "dist" / "macos"
WORK_DIR = common_config.PROJECT_ROOT / "build" / "temp" / "macos"
BUNDLE_NAME = f"{common_config.APP_NAME.replace(' ', '')}.app"
DMG_NAME = f"{common_config.APP_NAME.replace(' ', '')}-{common_config.VERSION}.dmg"

# macOS-specific PyInstaller settings
MACOS_PYINSTALLER_OPTIONS = {
    **common_config.COMMON_PYINSTALLER_OPTIONS,
    "name": common_config.APP_NAME.replace(' ', ''),
    "windowed": True,  # No console window
    "bundle_identifier": "com.friesen.enrollmentconverter",
}

# macOS-specific data files
def get_macos_data_files():
    """Get list of macOS-specific data files to include"""
    data_files = common_config.COMMON_DATA_FILES.copy()
    
    # Add macOS-specific icon files
    icon_files = [
        "icons/friesen_icon_macos.png",
        "icons/friesen_icon_128x128.png",
        "icons/friesen_icon_256x256.png",
        "icons/friesen_icon_512x512.png",
    ]
    
    for icon_file in icon_files:
        icon_path = common_config.PROJECT_ROOT / icon_file
        if icon_path.exists():
            data_files.append((str(icon_path), "icons"))
    
    return data_files

MACOS_DATA_FILES = get_macos_data_files()

# Icon file for macOS
MACOS_ICON_FILE = common_config.PROJECT_ROOT / "icons" / "friesen_icon_macos.png"

# macOS-specific Info.plist settings
MACOS_INFO_PLIST = {
    'CFBundleName': common_config.APP_NAME,
    'CFBundleDisplayName': common_config.APP_NAME,
    'CFBundleVersion': common_config.VERSION,
    'CFBundleShortVersionString': common_config.VERSION,
    'CFBundleExecutable': common_config.APP_NAME.replace(' ', ''),
    'CFBundleIdentifier': 'com.friesen.enrollmentconverter',
    'CFBundlePackageType': 'APPL',
    'CFBundleSignature': '????',
    'LSMinimumSystemVersion': '10.13.0',
    'NSHighResolutionCapable': True,
    'NSRequiresAquaSystemAppearance': False,
}

def validate_macos_environment():
    """Validate macOS-specific environment requirements"""
    # Check if we're on macOS
    if sys.platform != "darwin":
        raise RuntimeError("This build script is designed for macOS only")
    
    # Run common validation
    common_config.validate_environment()
    
    # Check for macOS-specific tools
    import subprocess
    
    # Check if create-dmg is available
    try:
        subprocess.run(["create-dmg", "--version"], check=True, capture_output=True)
        print("OK: create-dmg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: create-dmg not found. Install with: brew install create-dmg")
        print("   DMG creation will be skipped")
    
    print("OK: macOS environment validation passed") 