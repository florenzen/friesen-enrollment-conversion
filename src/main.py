import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from pathlib import Path

class ExcelConverterApp:
    def __init__(self):
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Excel File Converter")
        self.root.resizable(True, True)
        
        # Variables to store file paths
        self.selected_file_path = ""
        self.save_file_path = ""
        
        self.create_widgets()
        
        # Set size after widgets are created to ensure everything fits
        self.root.update_idletasks()  # Calculate required size
        self.root.geometry("800x700")  # Increased size to accommodate all content including full status text
        self.root.minsize(750, 650)    # Increased minimum size to ensure all content is always visible
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Excel File Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        # Open table section
        open_frame = ctk.CTkFrame(main_frame)
        open_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        open_label = ctk.CTkLabel(
            open_frame,
            text="Step 1: Select Excel File",
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
            text="Step 2: Convert File",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        convert_label.pack(pady=(20, 15))
        
        self.convert_button = ctk.CTkButton(
            convert_frame,
            text="Convert",
            command=self.convert_file,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"  # Disabled until file is selected
        )
        self.convert_button.pack(pady=(0, 20))
        
        # Status section
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=20, pady=(0, 30))  # Extra bottom padding
        
        status_title = ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_title.pack(anchor="w", padx=20, pady=(20, 8))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready - Please select an Excel file to begin",
            font=ctk.CTkFont(size=12),
            text_color="#00ff00"  # Green color for ready status
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 25))  # More bottom padding
        
    def open_file_dialog(self):
        """Open file dialog to select Excel file"""
        file_types = [
            ("Excel files", "*.xlsx *.xls"),
            ("Excel 2007+ files", "*.xlsx"),
            ("Excel Legacy files", "*.xls"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Excel file",
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
        """Open save dialog and copy/convert file"""
        if not self.selected_file_path:
            self.update_status("Please select a file first!", "#ff0000")
            return
        
        # Suggest filename based on original
        original_path = Path(self.selected_file_path)
        suggested_name = f"converted_{original_path.name}"
        
        file_types = [
            ("Excel files", "*.xlsx *.xls"),
            ("Excel 2007+ files", "*.xlsx"),
            ("Excel Legacy files", "*.xls"),
            ("All files", "*.*")
        ]
        
        # Let the native save dialog handle file replacement confirmation
        filename = filedialog.asksaveasfilename(
            title="Save converted file as",
            defaultextension=".xlsx",
            filetypes=file_types,
            initialfile=suggested_name,
            parent=self.root
        )
        
        if filename:  # User didn't cancel
            try:
                # For now, just copy the file (conversion logic will be added later)
                shutil.copy2(self.selected_file_path, filename)
                self.save_file_path = filename
                self.update_status(f"File converted successfully to: {Path(filename).name}", "#00ff00")
                print(f"File copied to: {filename}")
                
            except Exception as e:
                error_msg = f"Error saving file: {str(e)}"
                self.update_status(error_msg, "#ff0000")
                print(f"Error: {e}")
                
                # Show error message
                messagebox.showerror(
                    "Error", 
                    f"Failed to save file:\n{str(e)}",
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
    app = ExcelConverterApp()
    app.run()

if __name__ == "__main__":
    main() 