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

### Features

- **Modern GUI**: Built with CustomTkinter for a clean, modern appearance
- **Open table**: Click to select an Excel enrollment file (.xlsx or .xls) using a native file dialog
- **File path display**: Shows the path of the currently selected file in a read-only field
- **Convert to PDF**: Converts Excel enrollment data to a multi-page PDF with filled forms (one page per enrollment record)
- **Status updates**: Real-time feedback with color-coded status messages
- **Cross-platform**: Works on Windows, macOS, and Linux

### Interface

The application features a dark theme with:
- Rounded corners and modern styling
- Intuitive layout with clearly separated sections
- Disabled/enabled button states for better UX
- Success/error message dialogs
- Responsive design that adapts to window resizing

### Technical Details

- **GUI Framework**: CustomTkinter (modern tkinter alternative)
- **File Handling**: Native system file dialogs
- **Error Handling**: Comprehensive error handling with user feedback
- **Architecture**: Object-oriented design for maintainability

## Excel File Format

The application expects Excel files with the following columns:
- **Nachname** (required): Last name
- **Vorname** (required): First name  
- **Geburtsdatum** (optional): Date of birth
- **Kurs** (optional): Course/class information

## PDF Form Template

You can optionally place a PDF form template at `resources/form.pdf`. If no template is provided, the application will generate basic enrollment forms automatically.

## Building Windows Executable

To create a standalone Windows executable (.exe file):

### Prerequisites
- Windows machine or Windows VM
- Python 3.8+ installed
- Virtual environment activated with dependencies installed

### Build Process

1. **Navigate to project root:**
   ```cmd
   cd friesen-enrollment-conversion
   ```

2. **Run the build script:**
   ```cmd
   # Option 1: Use the batch file (recommended)
   build\windows\build.bat
   
   # Option 2: Run Python script directly  
   python build\windows\build.py
   ```

3. **Find your executable:**
   - The `.exe` file will be created in `dist/FriesenEnrollmentConverter.exe`
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