#!/usr/bin/env python3
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
Windows Build Script for Friesen Enrollment Converter

This script builds a single-file Windows executable using PyInstaller.
Run this script from the project root directory.

Usage:
    python build/windows/build.py
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Optional

# Import our build configuration
sys.path.insert(0, str(Path(__file__).parent))
from windows_config import *

class BuildError(Exception):
    """Custom exception for build errors"""
    pass

class WindowsBuilder:
    def __init__(self, version=None):
        self.project_root = PROJECT_ROOT
        self.build_dir = BUILD_DIR
        self.spec_file = self.build_dir / "FriesenEnrollmentConverter.spec"
        self.version = version or VERSION
        
    def validate_environment(self) -> None:
        """Validate that we can build"""
        print("Validating build environment...")
        
        # Check if we're on Windows (recommended) or if user knows what they're doing
        if platform.system() != "Windows":
            response = input("Warning: You're not on Windows. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                raise BuildError("Build cancelled - use Windows for best results")
        
        # Run common validation
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
        from build_config import validate_environment
        validate_environment()
    
    def install_build_dependencies(self) -> None:
        """Install build dependencies"""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
        from build_config import install_build_dependencies
        requirements_file = Path(__file__).parent.parent / "common" / "requirements-build.txt"
        install_build_dependencies(requirements_file)
    
    def clean_build_directories(self) -> None:
        """Clean previous build artifacts"""
        print("Cleaning previous build artifacts...")
        
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
        from build_config import clean_build_directories
        clean_build_directories(self.build_dir, DIST_DIR, WORK_DIR)
        
        # Remove spec file if it exists (we'll regenerate it)
        if self.spec_file.exists():
            self.spec_file.unlink()
            print(f"   Removed: {self.spec_file}")
        
        print("OK: Build directories cleaned")
    
    def _check_upx_available(self) -> bool:
        """Check if UPX compression is available"""
        try:
            subprocess.run(["upx", "--version"], check=True, capture_output=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def generate_spec_file(self) -> None:
        """Generate PyInstaller spec file"""
        print("Generating PyInstaller spec file...")
        
        # Check if UPX is available
        upx_available = self._check_upx_available()
        if upx_available:
            print("   UPX compression: Available - will compress executable")
        else:
            print("   UPX compression: Not available - executable will be larger")
        
        # Convert paths to use forward slashes (works on Windows) and ensure they're properly formatted
        main_script_path = str(MAIN_SCRIPT).replace('\\', '/')
        project_root_path = str(self.project_root).replace('\\', '/')
        icon_path = str(ICON_FILE).replace('\\', '/') if ICON_FILE else None
        
        # Debug output
        print(f"   Main script: {main_script_path}")
        print(f"   Project root: {project_root_path}")
        
        # Ensure proper Python boolean values
        upx_setting = "True" if upx_available else "False"
        console_setting = "False" if PYINSTALLER_OPTIONS["windowed"] else "True"
        
        # Create the spec file content with version info
        from windows_config import get_windows_version_info
        version_info = get_windows_version_info(self.version)
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable,
    StringStruct, VarFileInfo, VarStruct
)

block_cipher = None

a = Analysis(
    ['{main_script_path}'],
    pathex=['{project_root_path}', '{project_root_path}/src'],
    binaries=[],
    datas={DATA_FILES},
    hiddenimports={HIDDEN_IMPORTS},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={EXCLUDES},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{PYINSTALLER_OPTIONS["name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx={upx_setting},
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console_setting},
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={f"'{icon_path}'" if icon_path else None},
    version_file=None,
    version_info={version_info},
)
'''
        
        # Write spec file
        self.spec_file.write_text(spec_content)
        print(f"OK: Spec file generated: {self.spec_file}")
    
    def run_pyinstaller(self) -> None:
        """Run PyInstaller to build the executable"""
        print("Building executable with PyInstaller...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(self.spec_file),
            "--distpath", str(DIST_DIR),
            "--workpath", str(WORK_DIR),
        ]
        
        if PYINSTALLER_OPTIONS.get("clean"):
            cmd.append("--clean")
        
        if PYINSTALLER_OPTIONS.get("noconfirm"):
            cmd.append("--noconfirm")
        
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.project_root)
            print("OK: PyInstaller build completed")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: PyInstaller failed:")
            print(f"   STDOUT: {e.stdout}")
            print(f"   STDERR: {e.stderr}")
            raise BuildError("PyInstaller build failed")
    
    def validate_build_output(self) -> Path:
        """Validate that the executable was created successfully"""
        print("Validating build output...")
        
        exe_path = DIST_DIR / f"{PYINSTALLER_OPTIONS['name']}.exe"
        if not exe_path.exists():
            raise BuildError(f"Executable not found: {exe_path}")
        
        # Check file size (should be reasonable)
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"   Executable size: {size_mb:.1f} MB")
        
        if size_mb < 1:
            print("WARNING: Executable seems very small")
        elif size_mb > 200:
            print("WARNING: Executable seems very large")
        
        print(f"OK: Build output validated: {exe_path}")
        return exe_path
    
    def build(self, skip_deps: bool = False) -> Path:
        """Main build process"""
        print(f"Starting Windows build for {APP_NAME} v{self.version}")
        print(f"   Target: {EXE_NAME}")
        print(f"   Project root: {self.project_root}")
        print()
        
        try:
            self.validate_environment()
            if not skip_deps:
                self.install_build_dependencies()
            else:
                print("Skipping dependency installation...")
            self.clean_build_directories()
            self.generate_spec_file()
            self.run_pyinstaller()
            exe_path = self.validate_build_output()
            
            print()
            print("SUCCESS: Build completed successfully!")
            print(f"   Executable: {exe_path}")
            print(f"   Size: {exe_path.stat().st_size / (1024 * 1024):.1f} MB")
            print()
            print("Next steps:")
            print("   1. Test the executable on your target Windows machine")
            print("   2. Check that all features work correctly")
            print("   3. Distribute the single .exe file")
            
            return exe_path
            
        except BuildError as e:
            print(f"ERROR: Build failed: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nERROR: Build cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            sys.exit(1)

def main():
    """Entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        sys.exit(0)
    
    # Parse command line arguments
    skip_deps = "--skip-deps" in sys.argv
    
    # Extract version from command line
    version = None
    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
            break
    
    builder = WindowsBuilder(version=version)
    builder.build(skip_deps=skip_deps)

if __name__ == "__main__":
    main() 