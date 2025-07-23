# Friesen Enrollment Conversion

A Python application that converts Excel enrollment data to filled PDF forms.

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
   This installs: `openpyxl`, `pypdf`, `reportlab`, `customtkinter`


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
   - The `.exe` file will be created in `dist/windows/FriesenEnrollmentConverter.exe`
   - This is a single, portable file that can run on any Windows machine
   - No Python installation required on target machines
   - The executable will include your custom icon

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

## Automated Builds

The project includes GitHub Actions for automated Windows builds:

### **Release Process**
1. **Create a version tag:**
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

2. **GitHub Action automatically:**
   - Builds Windows executable on Windows runner
   - Creates GitHub Release with executable
   - Uploads build artifacts
   - Uses semantic versioning from tag

### **Version Management**
- **Local builds**: Use `0.0.1-dev` version (default)
- **Release builds**: Use semantic version from git tag (e.g., `v1.2.3` → `1.2.3`)
- **Version info**: Embedded in Windows executable properties 