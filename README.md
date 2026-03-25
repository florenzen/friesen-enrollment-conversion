# Friesen Enrollment Conversion

A Python GUI application that converts **CSV** or **Excel (.xlsx)** enrollment exports into filled PDF forms.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Friesen Enrollment Converter application:

```bash
python src/main.py
```

## Building Windows Executable

To create a standalone Windows executable (.exe file):

### Prerequisites
- Windows machine or Windows VM
- Python 3.8+ installed

### Build Process

1. **Navigate to project root:**
   ```cmd
   cd friesen-enrollment-conversion
   ```

2. **Install runtime dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```
   This installs: `customtkinter`, `pypdf`, `reportlab`, `openpyxl`, `charset-normalizer` (see `requirements.txt`).

3. **Run the build script:**
   ```cmd
   # Option 1: Use the batch file (recommended)
   build\windows\build.bat
   
   # Option 2: Run Python script directly  
   python build\windows\build.py
   ```
   
   **For local development** (uses version 0.0.1-dev):
   ```cmd
   build\windows\build.bat
   ```
   
   **For specific version** (for CI/CD):
   ```cmd
   build\windows\build.bat --version 1.2.3
   ```
   
   The build script will automatically install additional build-only dependencies (`pyinstaller`, etc.)

4. **Find your executable:**
   - Local builds write `dist/windows/FriesenEnrollmentConverter.exe` (single portable file; no Python needed on the target PC).
   - GitHub Actions renames the release artifact to `dist/windows/FriesenEnrollmentConverter-{version}.exe` before upload.
   - The executable includes the Windows icon assets from `icons/`.

### Build Features
- **Single file**: Everything bundled into one `.exe`
- **No console window**: Clean GUI-only application
- **Optimized size**: Excludes unnecessary modules
- **Error handling**: Clear build status and error messages
- **Validation**: Checks environment and output

### Troubleshooting
- Ensure you're running on Windows for best results
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- If build fails, check that your virtual environment is activated
- Antivirus software may flag the executable - add exception if needed

## Building macOS App Bundle

To create a standalone macOS app (`.app` bundle) and optionally a DMG installer:

### Prerequisites
- macOS (physical Mac or suitable VM)
- Python 3.8+ installed
- For DMG creation: [create-dmg](https://github.com/create-dmg/create-dmg) (e.g. `brew install create-dmg`). Without it, the build can still produce the app bundle; DMG steps are skipped with a warning.

### Build Process

1. **Navigate to project root:**
   ```bash
   cd friesen-enrollment-conversion
   ```

2. **Install runtime dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This installs: `customtkinter`, `pypdf`, `reportlab`, `openpyxl`, `charset-normalizer` (see `requirements.txt`).

3. **Run the build script:**
   ```bash
   # Option 1: From project root (recommended)
   python build/macos/build.py

   # Option 2: Shell wrapper (run from build/macos)
   cd build/macos
   ./build.sh
   ```

   **For local development** (uses version `0.0.1-dev`):
   ```bash
   python build/macos/build.py
   ```

   **For a specific version** (for CI/CD or releases):
   ```bash
   python build/macos/build.py --version 1.2.3
   ```

   **Optional flags:**
   - `--skip-deps` — do not install build dependencies (`pyinstaller`, etc.)
   - `--skip-codesign` — skip code signing
   - `--skip-dmg` — build the `.app` only, no DMG

   The build script installs additional build-only dependencies from `build/common/requirements-build.txt` unless you pass `--skip-deps`.

4. **Find your build output:**
   - **App bundle:** `dist/macos/FriesenEnrollmentConverter.app`
   - **DMG** (when `create-dmg` is available and DMG was not skipped): `dist/macos/FriesenEnrollmentConverter-{version}.dmg`
   - No Python installation required on target Macs for the bundled app
   - The app includes the macOS icon assets from `icons/`

### Build Features
- **Self-contained app bundle** with PyInstaller
- **Optional DMG** for distribution
- **Code signing** when a suitable developer identity is available (optional; skipped otherwise)
- **Validation**: Environment checks and build output verification

### Troubleshooting
- Run builds on macOS; PyInstaller cannot produce a macOS `.app` from Linux or Windows
- Install runtime deps: `pip install -r requirements.txt`
- If DMG creation fails: `brew install create-dmg`, or use `--skip-dmg` for an app-only build
- Gatekeeper may warn on unsigned builds; signing and notarization are project-specific (see `build/README.md` for more detail)

## Automated Builds

The project includes GitHub Actions for automated **Windows** and **macOS** builds.

### **Release Process**
1. **Create a version tag:**
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

2. **GitHub Actions automatically** (on `v*` tags, both workflows run in parallel):
   - **Windows** (`.github/workflows/build-windows.yml`): builds the `.exe`, renames it to `FriesenEnrollmentConverter-{version}.exe`, uploads an artifact, and attaches it to the GitHub Release for that tag.
   - **macOS** (`.github/workflows/build-macos.yml`): builds the DMG `FriesenEnrollmentConverter-{version}.dmg`, uploads an artifact, and attaches it to the same release.
   - Version is taken from the tag (`v1.2.3` → `1.2.3`).

### **Version Management**
- **Local builds**: Use `0.0.1-dev` version (default)
- **Release builds**: Use semantic version from git tag (e.g., `v1.2.3` → `1.2.3`)
- **Version info**: The Windows build embeds the `--version` value in the `.exe` properties (including CI). The macOS DMG filename uses `--version`; bundle `Info.plist` version keys follow `build/common/build_config.py` unless you adjust the macOS build to pass the CLI version into the plist.

