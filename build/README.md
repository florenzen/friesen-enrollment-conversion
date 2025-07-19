# Build System

This directory contains the build system for Friesen Enrollment Converter, supporting both Windows and macOS platforms.

## Structure

```
build/
├── common/                 # Shared build configuration and utilities
│   ├── __init__.py
│   ├── build_config.py    # Common configuration, validation, and utilities
│   └── requirements-build.txt  # Common build dependencies
├── windows/               # Windows-specific build files
│   ├── build.py          # Windows build script
│   ├── windows_config.py # Windows-specific configuration
│   ├── build.bat         # Windows batch file wrapper
│   └── __init__.py
├── macos/                 # macOS-specific build files
│   ├── build.py          # macOS build script
│   ├── macos_config.py   # macOS-specific configuration
│   ├── build.sh          # macOS shell script wrapper
│   └── __init__.py
└── README.md             # This file
```

## Common Configuration

The `common/build_config.py` file contains shared configuration and utilities:

- Project information (name, version, author, etc.)
- Common paths and directories
- Shared PyInstaller settings
- Common hidden imports and excludes
- Environment validation functions
- Build dependency installation
- Directory cleanup utilities

## Platform-Specific Builds

### Windows Build

Creates a single-file Windows executable (.exe).

**Requirements:**
- Python 3.8+
- PyInstaller
- Windows (recommended, but can run on other platforms)

**Usage:**
```bash
# From project root
python build/windows/build.py

# Or using the batch file
build/windows/build.bat

# With options
python build/windows/build.py --version 1.1.0 --skip-deps
```

**Options:**
- `--version VERSION`: Override version number
- `--skip-deps`: Skip dependency installation
- `--help`: Show help

### macOS Build

Creates a self-contained app bundle (.app) and optionally packages it into a DMG file.

**Requirements:**
- Python 3.8+
- PyInstaller
- create-dmg (for DMG creation)
- macOS

**Usage:**
```bash
# From project root
python build/macos/build.py

# Or using the shell script
cd build/macos
./build.sh

# With options
python build/macos/build.py --version 1.1.0 --skip-dmg
```

**Options:**
- `--version VERSION`: Override version number
- `--skip-deps`: Skip dependency installation
- `--skip-codesign`: Skip codesigning
- `--skip-dmg`: Skip DMG creation
- `--help`: Show help

## Build Process

Both build systems follow the same general process:

1. **Environment Validation**: Check Python version, dependencies, and platform requirements
2. **Dependency Installation**: Install build dependencies (PyInstaller, etc.)
3. **Cleanup**: Remove previous build artifacts
4. **Spec Generation**: Create PyInstaller spec file with platform-specific settings
5. **Build**: Run PyInstaller to create the executable/app bundle
6. **Validation**: Verify the build output
7. **Post-processing**: Codesign (macOS) and create DMG (macOS)

## Configuration

### Version Management

The version is defined in `common/build_config.py` and can be overridden via command line:

```python
VERSION = "0.0.1-dev"  # Default version
```

### Icons

- **Windows**: Uses `icons/friesen_icon.ico` and `icons/friesen_icon_128x128.png`
- **macOS**: Uses `icons/friesen_icon_macos.png` and various PNG sizes

### Data Files

Both platforms include:
- `resources/form.pdf` (if exists) - PDF form template
- Platform-specific icon files

## Output

### Windows
- **Location**: `dist/windows/FriesenEnrollmentConverter.exe`
- **Type**: Single-file executable
- **Size**: ~50-100 MB (depending on dependencies)

### macOS
- **App Bundle**: `dist/macos/FriesenEnrollmentConverter.app`
- **DMG**: `dist/macos/FriesenEnrollmentConverter-{version}.dmg`
- **Size**: ~100-200 MB (app bundle), ~50-100 MB (DMG)

## Recent Fixes

### Import Issues (Fixed)
- **Problem**: Circular import issues between platform-specific configs and common config
- **Solution**: Renamed platform config files to avoid naming conflicts:
  - `build/windows/build_config.py` → `build/windows/windows_config.py`
  - `build/macos/build_config.py` → `build/macos/macos_config.py`
- **Result**: Both Windows and macOS builds now work correctly with shared common configuration

### Version Parsing (Fixed)
- **Problem**: Development versions like `0.0.1-dev` couldn't be parsed for Windows version info
- **Solution**: Updated `get_version_info()` function to handle development versions by stripping suffixes
- **Result**: Both platforms can now handle semantic versioning with development suffixes

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r build/common/requirements-build.txt
   ```

2. **macOS: create-dmg not found**
   ```bash
   brew install create-dmg
   ```

3. **Windows: UPX not found**
   - UPX is optional and will be skipped if not available
   - Install UPX for smaller executables

4. **Codesigning Issues (macOS)**
   - Codesigning is optional and will be skipped if no developer identity is found
   - App will still work but may show security warnings

### Build Failures

1. Check that you're running from the project root directory
2. Ensure all runtime dependencies are installed
3. Verify Python version (3.8+)
4. Check platform requirements (Windows for Windows build, macOS for macOS build)

## Development

### Adding New Dependencies

1. Add to `requirements.txt` for runtime dependencies
2. Add to `build/{platform}/requirements-build.txt` for build dependencies
3. Update `common/build_config.py` if needed for hidden imports

### Modifying Build Configuration

1. **Common changes**: Edit `common/build_config.py`
2. **Windows-specific**: Edit `build/windows/windows_config.py`
3. **macOS-specific**: Edit `build/macos/macos_config.py`

### Testing Builds

Always test builds on the target platform:
- Windows builds should be tested on Windows
- macOS builds should be tested on macOS
- Check that all features work correctly in the bundled application 