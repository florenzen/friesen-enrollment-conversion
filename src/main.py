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

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from pathlib import Path

try:
    # Try relative import first (when run as a module)
    from .csv_converter import convert_enrollment_file_to_pdf
except ImportError:
    try:
        # Try absolute import (when run directly)
        from csv_converter import convert_enrollment_file_to_pdf
    except ImportError:
        # Handle case where converter dependencies are missing
        convert_enrollment_file_to_pdf = None

class FriesenEnrollmentConverterApp:
    def __init__(self):
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Friesen Enrollment Converter")
        self.root.resizable(True, True)
        
        # Set window icon - try multiple approaches for compatibility
        self._set_window_icon()
        
        # Variables to store file paths
        self.selected_file_path = ""
        self.save_file_path = ""
        
        # Debug mode variable
        self.debug_mode = tk.BooleanVar(value=False)  # Default to False (deselected)
        
        self.create_widgets()
        
        # Set size after widgets are created to ensure everything fits
        self.root.update_idletasks()  # Calculate required size
        self.root.geometry("800x840")
        self.root.minsize(750, 780)
    
    def _set_window_icon(self):
        """Set the window icon using multiple fallback methods"""
        try:
            # Get resource path - works both in development and when bundled
            def resource_path(relative_path):
                """Get absolute path to resource, works for dev and for PyInstaller"""
                import sys
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = getattr(sys, '_MEIPASS', Path(__file__).parent.parent)
                return Path(base_path) / relative_path
            
            # Try different icon files in order of preference
            icon_files = [
                "friesen_icon.ico",                # Bundled in exe root
                "icons/friesen_icon.ico",          # Development path
                "icons/friesen_icon_128x128.png",  # PNG fallback
            ]
            
            for icon_file in icon_files:
                try:
                    icon_path = resource_path(icon_file)
                    if icon_path.exists():
                        # Use wm_iconbitmap for .ico files (better Windows support)
                        if str(icon_path).endswith('.ico'):
                            self.root.wm_iconbitmap(str(icon_path))
                        else:
                            # Try regular iconbitmap for PNG
                            self.root.iconbitmap(str(icon_path))
                        print(f"Successfully loaded icon: {icon_path}")
                        return
                except Exception as e:
                    print(f"Failed to load icon {icon_file}: {e}")
                    continue
            
            print("No icon files found, using default icon")
            
        except Exception as e:
            print(f"Error setting window icon: {e}")
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Friesen Enrollment Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        # Open table section
        open_frame = ctk.CTkFrame(main_frame)
        open_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        open_label = ctk.CTkLabel(
            open_frame,
            text="Step 1: Select CSV or Excel enrollment file",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        open_label.pack(pady=(20, 15))
        
        self.open_button = ctk.CTkButton(
            open_frame,
            text="Open table",
            command=self.open_file_dialog,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.open_button.pack(pady=(0, 20))
        
        # File path section
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="Selected file:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        path_label.pack(anchor="w", padx=20, pady=(20, 8))
        
        self.file_path_entry = ctk.CTkEntry(
            path_frame,
            placeholder_text="No file selected...",
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.file_path_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        # Convert section
        convert_frame = ctk.CTkFrame(main_frame)
        convert_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        convert_label = ctk.CTkLabel(
            convert_frame,
            text="Step 2: Convert to PDF",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        convert_label.pack(pady=(20, 15))
        
        # Convert button and debug checkbox row
        convert_row = ctk.CTkFrame(convert_frame)
        convert_row.pack(pady=(0, 20))
        
        self.convert_button = ctk.CTkButton(
            convert_row,
            text="Convert",
            command=self.convert_file,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"  # Disabled until file is selected
        )
        self.convert_button.pack(side="left", padx=(0, 20))
        
        # Debug checkbox
        self.debug_checkbox = ctk.CTkCheckBox(
            convert_row,
            text="Debug",
            variable=self.debug_mode,
            font=ctk.CTkFont(size=12),
            checkbox_width=20,
            checkbox_height=20
        )
        self.debug_checkbox.pack(side="left", padx=(0, 0))
        
        # Debug help text
        debug_help = ctk.CTkLabel(
            convert_frame,
            text="Debug: Shows source column names as red labels in fields",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        )
        debug_help.pack(pady=(0, 0))
        
        # Status + errors: grows with window height so the log fills space to the bottom
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        status_title = ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_title.pack(anchor="w", padx=20, pady=(20, 8))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready - Please select a CSV or Excel (.xlsx) enrollment file to begin",
            font=ctk.CTkFont(size=12),
            text_color="#00ff00"  # Green color for ready status
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 12))
        
        # Error log (IBAN/BIC issues after Excel conversion; ~3 lines visible, scrollable)
        errors_header = ctk.CTkFrame(status_frame, fg_color="transparent")
        errors_header.pack(fill="x", padx=20, pady=(8, 4))
        errors_title = ctk.CTkLabel(
            errors_header,
            text="Errors:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        errors_title.pack(side="left", anchor="w")
        self.copy_errors_button = ctk.CTkButton(
            errors_header,
            text="Copy to clipboard",
            width=140,
            height=28,
            command=self._copy_errors_to_clipboard,
            font=ctk.CTkFont(size=12),
        )
        self.copy_errors_button.pack(side="right", anchor="e")
        
        # Minimum height ~3 lines; expands vertically with the window
        self.iban_issues_text = ctk.CTkTextbox(
            status_frame,
            height=100,
            font=ctk.CTkFont(size=11),
            text_color="#ff5555",
            wrap="word",
            activate_scrollbars=True,
        )
        self.iban_issues_text.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        self.iban_issues_text.insert("1.0", "")
        self.iban_issues_text.configure(state="disabled")
        
    def _copy_errors_to_clipboard(self) -> None:
        """Copy current error log text to the system clipboard."""
        try:
            content = self.iban_issues_text.get("1.0", "end-1c").strip()
            if not content:
                return
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update_idletasks()
        except tk.TclError:
            return
        self.update_status("Error list copied to clipboard.", "#00ff00")
        
    def _set_iban_log(self, text: str) -> None:
        """Replace read-only IBAN log content (errors in red, success line in green)."""
        self.iban_issues_text.configure(state="normal")
        self.iban_issues_text.delete("1.0", "end")
        if text.startswith("No validation errors") or text.startswith("no IBAN errors"):
            self.iban_issues_text.configure(text_color="#55dd88")
        else:
            self.iban_issues_text.configure(text_color="#ff5555")
        if text:
            self.iban_issues_text.insert("1.0", text)
        self.iban_issues_text.configure(state="disabled")
        
    def open_file_dialog(self):
        """Open file dialog to select CSV or Excel enrollment file"""
        file_types = [
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select enrollment file (CSV or Excel)",
            filetypes=file_types,
            parent=self.root
        )
        
        if filename:
            self.selected_file_path = filename
            # Enable entry temporarily to update text, then disable again
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)
            self.file_path_entry.configure(state="readonly")
            
            # Enable convert button
            self.convert_button.configure(state="normal")
            
            # Update status
            self.update_status(f"File selected: {Path(filename).name} - Ready to convert!", "#00ff00")
            print(f"Selected file: {filename}")
    
    def convert_file(self):
        """Open save dialog and convert enrollment file to PDF"""
        if not self.selected_file_path:
            self.update_status("Please select a file first!", "#ff0000")
            return
        
        # Suggest filename based on original (change to PDF)
        original_path = Path(self.selected_file_path)
        suggested_name = f"converted_{original_path.stem}.pdf"
        
        file_types = [
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
        
        # Let the native save dialog handle file replacement confirmation
        filename = filedialog.asksaveasfilename(
            title="Save converted PDF as",
            defaultextension=".pdf",
            filetypes=file_types,
            initialfile=suggested_name,
            parent=self.root
        )
        
        if filename:  # User didn't cancel
            try:
                # Check if converter is available
                if convert_enrollment_file_to_pdf is None:
                    self.update_status("Conversion dependencies not installed. Please install required packages.", "#ff0000")
                    messagebox.showerror(
                        "Missing Dependencies",
                        "PDF conversion requires additional packages.\n\nPlease install:\npip install reportlab openpyxl",
                        parent=self.root
                    )
                    return
                
                self.update_status("Converting to PDF...", "#ffaa00")
                self._set_iban_log("")
                
                validation_issues: list = []
                is_xlsx = original_path.suffix.lower() == ".xlsx"
                convert_enrollment_file_to_pdf(
                    self.selected_file_path,
                    filename,
                    debug=self.debug_mode.get(),
                    validation_issues=validation_issues if is_xlsx else None,
                )
                
                self.save_file_path = filename
                self.update_status(f"Successfully converted to PDF: {Path(filename).name}", "#00ff00")
                if is_xlsx:
                    if validation_issues:
                        self._set_iban_log("\n".join(validation_issues))
                    else:
                        self._set_iban_log("No validation errors.")
                else:
                    self._set_iban_log("")
                print(f"File converted to: {filename}")
                
            except Exception as e:
                error_msg = f"Conversion error: {str(e)}"
                self.update_status(error_msg, "#ff0000")
                print(f"Conversion error: {e}")
                
                # Show error message
                messagebox.showerror(
                    "Conversion Error", 
                    f"Failed to convert file:\n{str(e)}",
                    parent=self.root
                )
        else:
            # User cancelled the save operation
            self.update_status("Conversion cancelled by user", "#ffaa00")
    
    def update_status(self, message, color="#ffffff"):
        """Update status label with message and color"""
        self.status_label.configure(text=message, text_color=color)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    app = FriesenEnrollmentConverterApp()
    app.run()

if __name__ == "__main__":
    main() 