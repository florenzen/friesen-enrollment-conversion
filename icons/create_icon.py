#!/usr/bin/env python3
"""
Icon Generator for Friesen Enrollment Converter

Creates an application icon with:
- Table icon (left)
- Arrow pointing right
- PDF icon (right)
- Background based on logo.png (if exists)

Generates multiple sizes for Windows (.ico) and macOS compatibility.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_icon(size=512, background_color=(70, 130, 180)):
    """Create the application icon"""
    
    # Create main canvas
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create white background first
    img.paste((255, 255, 255, 255), (0, 0, size, size))
    
    # Try to load logo.png from current directory as background, otherwise use solid color
    logo_path = Path("logo.png")
    if logo_path.exists():
        try:
            logo = Image.open(logo_path)
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            # Maintain aspect ratio - fit logo inside square with padding
            logo_width, logo_height = logo.size
            if logo_width > logo_height:
                # Landscape: fit width, add padding top/bottom
                new_width = size
                new_height = int(size * logo_height / logo_width)
                logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center vertically
                paste_x = 0
                paste_y = (size - new_height) // 2
            else:
                # Portrait or square: fit height, add padding left/right  
                new_height = size
                new_width = int(size * logo_width / logo_height)
                logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center horizontally
                paste_x = (size - new_width) // 2
                paste_y = 0
            
            # Create a new image with white background for the logo
            logo_with_bg = Image.new('RGBA', (size, size), (255, 255, 255, 255))
            logo_with_bg.paste(logo, (paste_x, paste_y), logo)
            
            # Composite with main image
            img = Image.alpha_composite(img, logo_with_bg)
            draw = ImageDraw.Draw(img)
            
        except Exception as e:
            print(f"Could not load logo.png: {e}")
            # Fall back to white background (already set above)
    else:
        print("logo.png not found, using white background")
    
    # Calculate positions and sizes based on icon size
    margin = size // 8
    icon_size = size // 4
    arrow_width = size // 6
    
    # Table icon position (top-left area)
    table_x = margin
    table_y = margin
    
    # PDF icon position (top-right area)
    pdf_x = size - margin - icon_size
    pdf_y = margin
    
    # Arrow position (center between icons, tip moved slightly right)
    arrow_start_x = table_x + icon_size + margin // 2
    arrow_end_x = pdf_x - margin // 2
    arrow_y = table_y + icon_size // 2
    
    # Draw table icon (3 columns, 6 rows like a text table)
    table_color = (50, 50, 50, 255)  # Dark gray for borders
    cell_width = icon_size // 3
    cell_height = icon_size // 6
    
    # Table background - white like a document
    draw.rectangle([table_x, table_y, table_x + icon_size, table_y + icon_size], 
                  fill=(255, 255, 255, 255), outline=table_color, width=1)
    
    # Table grid lines - 3 columns, 6 rows
    # Vertical lines (column separators)
    for i in range(1, 3):
        x = table_x + i * cell_width
        draw.line([(x, table_y), (x, table_y + icon_size)], fill=table_color, width=1)
    
    # Horizontal lines (row separators)
    for i in range(1, 6):
        y = table_y + i * cell_height
        draw.line([(table_x, y), (table_x + icon_size, y)], fill=table_color, width=1)
    
    # Add text-like content to cells (dots and lines to mimic text)
    text_color = (0, 0, 0, 255)  # Black for text
    
    for row in range(6):
        for col in range(3):
            cell_x = table_x + col * cell_width
            cell_y = table_y + row * cell_height
            cell_center_x = cell_x + cell_width // 2
            cell_center_y = cell_y + cell_height // 2
            
            # Add different patterns to simulate text content
            if row == 0:  # Header row - thicker lines
                line_length = cell_width * 0.6
                line_y = cell_center_y
                draw.line([(cell_center_x - line_length//2, line_y), 
                          (cell_center_x + line_length//2, line_y)], 
                         fill=text_color, width=2)
            else:  # Data rows - dots and short lines
                if col == 0:  # First column - dots (like bullet points)
                    dot_radius = max(1, cell_height // 8)
                    draw.ellipse([cell_center_x - dot_radius, cell_center_y - dot_radius,
                                cell_center_x + dot_radius, cell_center_y + dot_radius], 
                               fill=text_color)
                else:  # Other columns - lines of varying length (like text)
                    line_length = cell_width * (0.4 + (row + col) % 3 * 0.2)  # Varying lengths
                    line_y = cell_center_y
                    draw.line([(cell_center_x - line_length//2, line_y), 
                              (cell_center_x + line_length//2, line_y)], 
                             fill=text_color, width=1)
    
    # Draw PDF icon - completely red with white letters
    pdf_bg_color = (220, 50, 50, 255)  # Solid red background
    pdf_text_color = (255, 255, 255, 255)  # Pure white text
    pdf_border_color = (180, 40, 40, 255)  # Darker red border
    
    # PDF document shape - solid red background
    corner_size = icon_size // 6
    draw.rectangle([pdf_x, pdf_y, pdf_x + icon_size, pdf_y + icon_size], 
                  fill=pdf_bg_color, outline=pdf_border_color, width=2)
    
    # Folded corner - darker red
    draw.polygon([pdf_x + icon_size - corner_size, pdf_y,
                 pdf_x + icon_size, pdf_y,
                 pdf_x + icon_size, pdf_y + corner_size], 
                fill=pdf_border_color)
    
    # PDF text - draw VERY BOLD white "PDF" letters that fill the icon
    # Use manual drawing for maximum visibility
    char_width = icon_size // 3.0    # Make letters even wider
    char_height = icon_size * 0.75    # Make letters taller 
    stroke_width = max(4, icon_size // 15)  # Much thicker strokes for bold effect
    
    # Calculate total width and center the letters
    total_width = char_width * 3
    start_x = pdf_x + (icon_size - total_width) // 2
    start_y = pdf_y + (icon_size - char_height) // 2
    
    # BOLD white block letters "PDF" that dominate the icon
    for i, char in enumerate(['P', 'D', 'F']):
        char_x = start_x + i * char_width
        if char == 'P':
            # Draw P - thick vertical stroke and two thick horizontal bars
            draw.rectangle([char_x, start_y, char_x + stroke_width, start_y + char_height], fill=pdf_text_color)
            draw.rectangle([char_x, start_y, char_x + char_width*0.9, start_y + stroke_width], fill=pdf_text_color)
            draw.rectangle([char_x, start_y + char_height//2.1, char_x + char_width*0.8, start_y + char_height//2.1 + stroke_width], fill=pdf_text_color)
            draw.rectangle([char_x + char_width*0.75, start_y, char_x + char_width*0.9, start_y + char_height//1.9], fill=pdf_text_color)
        elif char == 'D':
            # Draw D - thick vertical stroke and curved shape
            draw.rectangle([char_x, start_y, char_x + stroke_width, start_y + char_height], fill=pdf_text_color)
            draw.rectangle([char_x, start_y, char_x + char_width*0.8, start_y + stroke_width], fill=pdf_text_color)
            draw.rectangle([char_x, start_y + char_height - stroke_width, char_x + char_width*0.8, start_y + char_height], fill=pdf_text_color)
            draw.rectangle([char_x + char_width*0.75, start_y + stroke_width, char_x + char_width*0.9, start_y + char_height - stroke_width], fill=pdf_text_color)
        elif char == 'F':
            # Draw F - thick vertical stroke and two thick horizontal bars
            draw.rectangle([char_x, start_y, char_x + stroke_width, start_y + char_height], fill=pdf_text_color)
            draw.rectangle([char_x, start_y, char_x + char_width*0.9, start_y + stroke_width], fill=pdf_text_color)
            draw.rectangle([char_x, start_y + char_height//2.1, char_x + char_width*0.7, start_y + char_height//2.1 + stroke_width], fill=pdf_text_color)
    
    # Draw arrow
    arrow_color = (255, 215, 0, 255)  # Gold color
    arrow_thickness = max(2, size // 128)
    
    # Arrow shaft
    draw.line([(arrow_start_x, arrow_y), (arrow_end_x, arrow_y)], 
             fill=arrow_color, width=arrow_thickness * 2)
    
    # Arrow head
    head_size = arrow_width // 3
    draw.polygon([
        (arrow_end_x + head_size // 2, arrow_y),
        (arrow_end_x - head_size, arrow_y - head_size // 2),
        (arrow_end_x - head_size, arrow_y + head_size // 2)
    ], fill=arrow_color)
    
    return img

def save_icon_formats(base_img, name="friesen_icon"):
    """Save icon in multiple formats and sizes"""
    
    # Common icon sizes
    sizes = [128, 256, 512]
    
    images = []
    
    # Generate all sizes
    for size in sizes:
        if size <= 512:
            resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
            
            # Save individual PNG files
            png_path = f"{name}_{size}x{size}.png"
            resized.save(png_path, "PNG")
            print(f"Created: {png_path}")
    
    # Save as ICO file for Windows
    ico_path = f"{name}.ico"
    images[1].save(ico_path, format='ICO', sizes=[(img.size[0], img.size[0]) for img in images])
    print(f"Created: {ico_path}")
    
    # Save high-res PNG for macOS conversion
    macos_path = f"{name}_macos.png"
    base_img.save(macos_path, "PNG")
    print(f"Created: {macos_path} (use this for macOS .icns conversion)")
    
    return ico_path, macos_path

def main():
    print("🎨 Creating Friesen Enrollment Converter icon...")
    
    # Create base icon at high resolution
    icon = create_icon(512)
    
    # Save in various formats
    ico_path, macos_path = save_icon_formats(icon)
    
    print("\n✅ Icon generation complete!")
    print(f"📁 All icons saved in: {Path('icons').absolute()}")
    print("\n📋 Files created:")
    print(f"   • {ico_path} - Windows executable icon")
    print(f"   • {macos_path} - macOS icon source (convert to .icns)")
    
    print("\n🔧 Next steps:")
    print("   1. The .ico file is ready for Windows builds")
    print("   2. For macOS: convert the _macos.png to .icns using:")
    print("      iconutil -c icns friesen_icon_macos.png")
    print("   3. Update build configuration to use these icons")

if __name__ == "__main__":
    main() 