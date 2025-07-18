# Friesen Enrollment Conversion

A simple Python project with a modern GUI for Excel file conversion.

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

Run the Excel File Converter application:

```bash
python src/main.py
```

### Features

- **Modern GUI**: Built with CustomTkinter for a clean, modern appearance
- **Open table**: Click to select an Excel file (.xlsx or .xls) using a native file dialog
- **File path display**: Shows the path of the currently selected file in a read-only field
- **Convert**: Saves the selected Excel file to a new location (currently just copies the file)
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