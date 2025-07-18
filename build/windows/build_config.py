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
from pathlib import Path

# Project information
PROJECT_NAME = "friesen-enrollment-conversion"
APP_NAME = "Friesen Enrollment Converter"
VERSION = "1.0.0"
AUTHOR = "Florian Lorenzen"
DESCRIPTION = "Friesen Enrollment Converter - Convert and process enrollment files"

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
MAIN_SCRIPT = SRC_DIR / "main.py"
BUILD_DIR = PROJECT_ROOT / "build" / "windows"
DIST_DIR = PROJECT_ROOT / "dist"
WORK_DIR = PROJECT_ROOT / "build" / "temp"

# PyInstaller settings
PYINSTALLER_OPTIONS = {
    "name": "FriesenEnrollmentConverter",
    "onefile": True,
    "windowed": True,  # No console window
    "clean": True,
    "noconfirm": True,
    "collect_all": ["openpyxl", "pypdf", "reportlab", "customtkinter"],
}

# CustomTkinter and PDF conversion specific settings
HIDDEN_IMPORTS = [
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
EXCLUDES = [
    "matplotlib",
    "numpy",
    "scipy",
    "jupyter",
    "IPython",
    "notebook",
    "pytest",
    # Don't exclude setuptools/pip as they might be needed by dependencies
]

# Data files to include (if any)
def get_data_files():
    """Get list of data files to include, checking if they exist"""
    data_files = [
        # Include the icon file in the exe
        (str(PROJECT_ROOT / "icons" / "friesen_icon.ico"), "."),
        (str(PROJECT_ROOT / "icons" / "friesen_icon_128x128.png"), "."),
    ]
    
    # Include the PDF form template if it exists
    form_pdf = PROJECT_ROOT / "resources" / "form.pdf"
    if form_pdf.exists():
        data_files.append((str(form_pdf), "resources"))
    
    return data_files

DATA_FILES = get_data_files()

# Icon file (path to .ico file)
ICON_FILE = PROJECT_ROOT / "icons" / "friesen_icon.ico"

# Build output
EXE_NAME = f"{APP_NAME.replace(' ', '')}.exe"

def get_version_info():
    """Return version info for Windows executable"""
    return f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
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
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'{EXE_NAME}'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
""".format(
        AUTHOR=AUTHOR,
        DESCRIPTION=DESCRIPTION,
        VERSION=VERSION,
        APP_NAME=APP_NAME,
        EXE_NAME=EXE_NAME
    ) 