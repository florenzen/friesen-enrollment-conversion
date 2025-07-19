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
macOS Build Script for Friesen Enrollment Converter

This script builds a self-contained macOS app bundle and packages it into a DMG file.
Run this script from the project root directory.

Usage:
    python build/macos/build.py
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
from macos_config import (
    PROJECT_ROOT, APP_NAME, VERSION, BUILD_DIR, BUNDLE_NAME, DMG_NAME,
    MACOS_PYINSTALLER_OPTIONS, MACOS_DATA_FILES, MACOS_ICON_FILE, MACOS_INFO_PLIST,
    COMMON_HIDDEN_IMPORTS, COMMON_EXCLUDES, MAIN_SCRIPT, DIST_DIR, WORK_DIR
)

class BuildError(Exception):
    """Custom exception for build errors"""
    pass

class MacOSBuilder:
    def __init__(self, version=None):
        self.project_root = PROJECT_ROOT
        self.build_dir = BUILD_DIR
        self.spec_file = self.build_dir / f"{APP_NAME.replace(' ', '')}.spec"
        self.version = version or VERSION
        
    def validate_environment(self) -> None:
        """Validate that we can build"""
        print("Validating build environment...")
        
        # Check if we're on macOS
        if platform.system() != "Darwin":
            raise BuildError("This build script is designed for macOS only")
        
        # Run common validation
        from macos_config import common_config
        common_config.validate_environment()
        
        # Check for macOS-specific tools
        try:
            subprocess.run(["create-dmg", "--version"], check=True, capture_output=True)
            print("OK: create-dmg found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("WARNING: create-dmg not found. Install with: brew install create-dmg")
            print("   DMG creation will be skipped")
        
        print("OK: macOS environment validation passed")
    
    def install_build_dependencies(self) -> None:
        """Install build dependencies"""
        from macos_config import common_config
        requirements_file = Path(__file__).parent.parent / "common" / "requirements-build.txt"
        common_config.install_build_dependencies(requirements_file)
    
    def clean_build_directories(self) -> None:
        """Clean previous build artifacts"""
        print("Cleaning previous build artifacts...")
        
        from macos_config import common_config
        common_config.clean_build_directories(self.build_dir, DIST_DIR, WORK_DIR)
        
        # Remove spec file if it exists (we'll regenerate it)
        if self.spec_file.exists():
            self.spec_file.unlink()
            print(f"   Removed: {self.spec_file}")
        
        print("OK: Build directories cleaned")
    
    def generate_spec_file(self) -> None:
        """Generate PyInstaller spec file for macOS app bundle"""
        print("Generating PyInstaller spec file...")
        
        # Convert paths to use forward slashes and ensure they're properly formatted
        main_script_path = str(MAIN_SCRIPT).replace('\\', '/')
        project_root_path = str(self.project_root).replace('\\', '/')
        icon_path = str(MACOS_ICON_FILE).replace('\\', '/') if MACOS_ICON_FILE.exists() else None
        
        # Debug output
        print(f"   Main script: {main_script_path}")
        print(f"   Project root: {project_root_path}")
        print(f"   Icon file: {icon_path}")
        
        # Create the spec file content
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_script_path}'],
    pathex=['{project_root_path}', '{project_root_path}/src'],
    binaries=[],
    datas={MACOS_DATA_FILES},
    hiddenimports={COMMON_HIDDEN_IMPORTS},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={COMMON_EXCLUDES},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{APP_NAME.replace(' ', '')}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME.replace(' ', '')}',
)

app = BUNDLE(
    coll,
    name='{BUNDLE_NAME}',
    icon={f"'{icon_path}'" if icon_path else None},
    bundle_identifier='{MACOS_PYINSTALLER_OPTIONS["bundle_identifier"]}',
    info_plist={MACOS_INFO_PLIST},
)
'''
        
        # Write spec file
        self.spec_file.write_text(spec_content)
        print(f"OK: Spec file generated: {self.spec_file}")
    
    def run_pyinstaller(self) -> None:
        """Run PyInstaller to build the app bundle"""
        print("Building app bundle with PyInstaller...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(self.spec_file),
            "--distpath", str(DIST_DIR),
            "--workpath", str(WORK_DIR),
        ]
        
        if MACOS_PYINSTALLER_OPTIONS.get("clean"):
            cmd.append("--clean")
        
        if MACOS_PYINSTALLER_OPTIONS.get("noconfirm"):
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
    
    def validate_app_bundle(self) -> Path:
        """Validate that the app bundle was created successfully"""
        print("Validating app bundle...")
        
        app_path = DIST_DIR / BUNDLE_NAME
        if not app_path.exists():
            raise BuildError(f"App bundle not found: {app_path}")
        
        # Check basic structure
        required_items = [
            "Contents/MacOS",
            "Contents/Resources",
            "Contents/Info.plist"
        ]
        
        for item in required_items:
            item_path = app_path / item
            if not item_path.exists():
                raise BuildError(f"Missing required item: {item}")
        
        # Check executable
        executable_path = app_path / "Contents/MacOS" / APP_NAME.replace(' ', '')
        if not executable_path.exists():
            raise BuildError(f"Missing executable: {executable_path}")
        
        # Check if executable is actually executable
        if not os.access(executable_path, os.X_OK):
            raise BuildError(f"Executable is not executable: {executable_path}")
        
        # Check file size (should be reasonable)
        size_mb = app_path.stat().st_size / (1024 * 1024)
        print(f"   App bundle size: {size_mb:.1f} MB")
        
        if size_mb < 10:
            print("WARNING: App bundle seems very small")
        elif size_mb > 500:
            print("WARNING: App bundle seems very large")
        
        print(f"OK: App bundle validated: {app_path}")
        return app_path
    
    def codesign_app(self, app_path: Path) -> None:
        """Codesign the app bundle (optional, for distribution)"""
        print("Codesigning app bundle...")
        
        # Check if we have a valid developer identity
        try:
            result = subprocess.run(
                ["security", "find-identity", "-v", "-p", "codesigning"],
                capture_output=True, text=True, check=True
            )
            
            if "Developer ID Application" in result.stdout or "Apple Development" in result.stdout:
                print("OK: Developer identity found, codesigning app...")
                
                cmd = [
                    "codesign", "--force", "--deep", "--sign", "-",
                    str(app_path)
                ]
                
                try:
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    print("OK: App bundle codesigned")
                except subprocess.CalledProcessError as e:
                    print(f"WARNING: Codesigning failed: {e}")
                    print("   App will still work, but may show security warnings")
            else:
                print("WARNING: No developer identity found, skipping codesigning")
                print("   App will still work, but may show security warnings")
        
        except subprocess.CalledProcessError:
            print("WARNING: Could not check for developer identity, skipping codesigning")
    
    def create_dmg(self, app_path: Path) -> Optional[Path]:
        """Create DMG file containing the app bundle"""
        print(f"Creating DMG file: {DMG_NAME}")
        
        # Check if create-dmg is available
        try:
            subprocess.run(["create-dmg", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("WARNING: create-dmg not found, skipping DMG creation")
            print("   Install with: brew install create-dmg")
            return None
        
        # Create temporary directory for DMG contents
        dmg_temp_dir = self.project_root / "dmg_temp"
        if dmg_temp_dir.exists():
            shutil.rmtree(dmg_temp_dir)
        dmg_temp_dir.mkdir()
        
        try:
            # Copy app bundle to temp directory
            shutil.copytree(app_path, dmg_temp_dir / BUNDLE_NAME)
            
            # Create Applications symlink
            os.symlink("/Applications", dmg_temp_dir / "Applications")
            
            # Create DMG
            dmg_path = DIST_DIR / DMG_NAME
            cmd = [
                "create-dmg",
                "--volname", APP_NAME,
                "--volicon", str(MACOS_ICON_FILE) if MACOS_ICON_FILE.exists() else "",
                "--window-pos", "200", "120",
                "--window-size", "600", "400",
                "--icon-size", "100",
                "--icon", BUNDLE_NAME, "175", "120",
                "--hide-extension", BUNDLE_NAME,
                "--app-drop-link", "425", "120",
                str(dmg_path),
                str(dmg_temp_dir)
            ]
            
            # Remove empty volicon if icon doesn't exist
            if not MACOS_ICON_FILE.exists():
                cmd = [arg for arg in cmd if arg != "--volicon" and arg != str(MACOS_ICON_FILE)]
            
            print(f"   Command: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print("OK: DMG file created")
            except subprocess.CalledProcessError as e:
                # create-dmg sometimes returns non-zero exit code but still creates the file
                print(f"WARNING: create-dmg returned exit code {e.returncode}")
                print("   Checking if DMG was created anyway...")
            
            # Check if DMG was created (it might have a temporary name)
            if dmg_path.exists():
                dmg_size_mb = dmg_path.stat().st_size / (1024 * 1024)
                print(f"   DMG size: {dmg_size_mb:.1f} MB")
                return dmg_path
            else:
                # Check for temporary DMG files
                temp_dmg_pattern = f"rw.*{DMG_NAME}"
                temp_dmg_files = list(DIST_DIR.glob(temp_dmg_pattern))
                if temp_dmg_files:
                    temp_dmg_path = temp_dmg_files[0]
                    # Rename to final name
                    temp_dmg_path.rename(dmg_path)
                    dmg_size_mb = dmg_path.stat().st_size / (1024 * 1024)
                    print(f"   DMG size: {dmg_size_mb:.1f} MB")
                    return dmg_path
                else:
                    raise BuildError("DMG file not created")
                
        finally:
            # Clean up temp directory
            if dmg_temp_dir.exists():
                shutil.rmtree(dmg_temp_dir)
    
    def build(self, skip_deps: bool = False, skip_codesign: bool = False, skip_dmg: bool = False) -> tuple[Path, Optional[Path]]:
        """Main build process"""
        print(f"Starting macOS build for {APP_NAME} v{self.version}")
        print(f"   Target: {BUNDLE_NAME}")
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
            app_path = self.validate_app_bundle()
            
            if not skip_codesign:
                self.codesign_app(app_path)
            else:
                print("Skipping codesigning...")
            
            dmg_path = None
            if not skip_dmg:
                dmg_path = self.create_dmg(app_path)
            else:
                print("Skipping DMG creation...")
            
            print()
            print("SUCCESS: Build completed successfully!")
            print(f"   App bundle: {app_path}")
            if dmg_path:
                print(f"   DMG file: {dmg_path}")
            print()
            print("Next steps:")
            print("   1. Test the app bundle on your target macOS machine")
            print("   2. Check that all features work correctly")
            if dmg_path:
                print("   3. Distribute the DMG file")
            else:
                print("   3. Distribute the app bundle")
            
            return app_path, dmg_path
            
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
    skip_codesign = "--skip-codesign" in sys.argv
    skip_dmg = "--skip-dmg" in sys.argv
    
    # Extract version from command line
    version = None
    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
            break
    
    builder = MacOSBuilder(version=version)
    builder.build(skip_deps=skip_deps, skip_codesign=skip_codesign, skip_dmg=skip_dmg)

if __name__ == "__main__":
    main() 