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
Build configuration for Windows executable
"""
import os
import sys
from pathlib import Path

# Import common configuration
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
import build_config as common_config

# Re-export common variables for easier access
PROJECT_ROOT = common_config.PROJECT_ROOT
APP_NAME = common_config.APP_NAME
VERSION = common_config.VERSION
DESCRIPTION = common_config.DESCRIPTION
AUTHOR = common_config.AUTHOR
MAIN_SCRIPT = common_config.MAIN_SCRIPT
COMMON_PYINSTALLER_OPTIONS = common_config.COMMON_PYINSTALLER_OPTIONS
COMMON_HIDDEN_IMPORTS = common_config.COMMON_HIDDEN_IMPORTS
COMMON_EXCLUDES = common_config.COMMON_EXCLUDES
COMMON_DATA_FILES = common_config.COMMON_DATA_FILES
get_version_info = common_config.get_version_info

# Windows-specific paths
BUILD_DIR = PROJECT_ROOT / "build" / "windows"
DIST_DIR = PROJECT_ROOT / "dist" / "windows"
WORK_DIR = PROJECT_ROOT / "build" / "temp" / "windows"

# Windows-specific PyInstaller settings
PYINSTALLER_OPTIONS = {
    **COMMON_PYINSTALLER_OPTIONS,
    "name": "FriesenEnrollmentConverter",
    "onefile": True,
    "windowed": True,  # No console window
}

# Use common hidden imports and excludes
HIDDEN_IMPORTS = COMMON_HIDDEN_IMPORTS
EXCLUDES = COMMON_EXCLUDES

# Windows-specific data files
def get_windows_data_files():
    """Get list of Windows-specific data files to include"""
    data_files = COMMON_DATA_FILES.copy()
    
    # Add Windows-specific icon files
    icon_files = [
        "icons/friesen_icon.ico",
        "icons/friesen_icon_128x128.png",
    ]
    
    for icon_file in icon_files:
        icon_path = PROJECT_ROOT / icon_file
        if icon_path.exists():
            data_files.append((str(icon_path), "."))
    
    return data_files

DATA_FILES = get_windows_data_files()

# Icon file (path to .ico file)
ICON_FILE = PROJECT_ROOT / "icons" / "friesen_icon.ico"

# Build output
EXE_NAME = f"{APP_NAME.replace(' ', '')}.exe"

def get_windows_version_info(version=None):
    """Return version info for Windows executable"""
    version_info = get_version_info(version)
    
    return f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_info['major']}, {version_info['minor']}, {version_info['patch']}, {version_info['build']}),
    prodvers=({version_info['major']}, {version_info['minor']}, {version_info['patch']}, {version_info['build']}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{AUTHOR}'),
        StringStruct(u'FileDescription', u'{DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{version_info["version"]}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'{EXE_NAME}'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{version_info["version"]}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
""" 