"""
CSV Converter Module

This module provides functionality to read CSV files with Windows 1252 encoding
and semicolon separators, converting them to a list of dictionaries where
the first row serves as the dictionary keys.
"""

import csv
import sys
from typing import List, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, grey, Color
from reportlab.pdfgen import canvas

key_mapping = {
    'id': None,
    'sorting': None,
    'form': None,
    'date': None,
    'ip': None,
    'fd_member': None,
    'fd_user': None,
    'fd_member_group': None,
    'fd_user_group': None,
    'published': None,
    'alias': None,
    'confirmationSent': None,
    'confirmationDate': None,
    'be_notes': None,
    'Angebot': 'goal',
    'von': 'from',
    'bis': 'to',
    'Beitrag': None,
    'Unterricht': None,
    'Vorkentnisse': 'previous_knowledge',
    'Geschlecht': 'sex',
    'Teilnehmer-Name': 'last_name',
    'Teilnehmer-Vorname': 'first_name',
    'Geburtsdatum': 'birth_date',
    'Strasse_Teilnehmer': 'street',
    'PLZ_Teilnehmer': 'zip',
    'Ort_Teilnehmer': 'city',
    'Telefon': 'phone',
    'E-Mail': 'email',
    'Beruf': 'profession',
    'Vereinsmitglied': 'is_member',
    'Vereinsmitglied_Mitgliedsnummer': 'member_id',
    'Ermaessigung': 'discount',
    'Familienmitglied': 'family_member',
    'Mitglieder_Haushalt': 'household_members',
    'Geschlecht_Antragsteller': 'applicant_sex',
    'Name-Antragsteller': 'applicant_last_name',
    'Vorname-Antragsteller': 'applicant_first_name',
    'Strasse_Antragsteller': 'applicant_street',
    'PLZ_Antragsteller': 'applicant_zip',
    'Ort_Antragsteller': 'applicant_city',
    'check-Sportgesundheit': None,
    'check-Datenschutz': None,
    'check-Coronaschutz': None,
    'Kontoinhaber': 'account_holder',
    'Kreditinstitut': 'bank_name',
    'IBAN': 'iban',
    'BIC': 'bic'
}

def read_csv_to_dicts(filename: str) -> List[Dict[str, Any]]:
    """
    Read a CSV file with Windows 1252 encoding and semicolon separators,
    returning a list of dictionaries where the first row contains the keys.
    
    Args:
        filename (str): Path to the CSV file to read
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries, each representing a row
                              with column headers as keys
                              
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        UnicodeDecodeError: If the file cannot be decoded with Windows 1252 encoding
        Exception: For other CSV parsing errors
    """
    try:
        with open(filename, 'r', encoding='windows-1252', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Failed to decode file '{filename}' with Windows 1252 encoding: {e}")
    except Exception as e:
        raise Exception(f"Error reading CSV file '{filename}': {e}")


def generate_pdf_from_dict(data_dict: Dict[str, Any], c: canvas.Canvas) -> None:
    """
    Generate a one-page PDF from a dictionary row with specific formatting.
    
    Args:
        data_dict (Dict[str, Any]): Dictionary containing the row data
        c (canvas.Canvas): Canvas object to draw on
        
    Raises:
        Exception: If there's an error creating the PDF
    """
    try:
        
        # Define a very light grey color (95% white, 5% black)
        light_grey = Color(0.95, 0.95, 0.95)
        
        def draw_text_in_box(text, x, y, box_width, font_name="Helvetica", base_font_size=12, padding=5):
            """
            Draw text in a box with automatic font size reduction if needed.
            
            Args:
                text: Text to draw
                x, y: Position coordinates
                box_width: Width of the box
                font_name: Font family name
                base_font_size: Starting font size
                padding: Padding from box edges
            """
            if not text:
                return
            
            # Calculate available width for text
            available_width = box_width - (2 * padding)
            
            # Start with base font size
            font_size = base_font_size
            
            # Reduce font size until text fits
            while font_size > 6:  # Minimum font size of 6pt
                c.setFont(font_name, font_size)
                text_width = c.stringWidth(text, font_name, font_size)
                if text_width <= available_width:
                    break
                font_size -= 1
            
            # Draw the text
            c.drawString(x + padding, y, text)
        
        # Set margins
        margin_top = 1.5 * cm
        margin_bottom = 1.5 * cm
        margin_left = 2 * cm
        margin_right = 2 * cm
        
        # Calculate usable area
        usable_width = A4[0] - margin_left - margin_right
        usable_height = A4[1] - margin_top - margin_bottom
        
        # Start position (top-left of usable area)
        x = margin_left
        y = A4[1] - margin_top
        
        # Main title - centered, bold, 20pt
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(black)
        title_text = "Berliner Schwimmverein „Friesen 1895“ e. V."
        title_width = c.stringWidth(title_text, "Helvetica-Bold", 20)
        c.drawString((A4[0] - title_width) / 2, y, title_text)
        
        # Move down for subtitle
        y -= 40
        
        # Subtitle - centered, bold, 14pt
        c.setFont("Helvetica-Bold", 14)
        subtitle_text = "Aufnahmeantrag (konvertiert)"
        subtitle_width = c.stringWidth(subtitle_text, "Helvetica-Bold", 14)
        c.drawString((A4[0] - subtitle_width) / 2, y, subtitle_text)
        
        # Add three boxes at the top
        # Calculate box dimensions
        top_box_width = 4 * cm
        top_box_height = 1.2 * cm  # Same height as other grey boxes
        top_box_gap = 1 * mm  # 1mm gap between boxes
        
        # Calculate positions aligned with left margin
        # First box: "Unterrichtsziel" - aligned with left margin
        unterrichtszie_x = x  # Align with left margin
        unterrichtszie_y = y + 5  # Slightly above subtitle baseline
        
        # Draw first box with light grey fill
        c.setFillColor(light_grey)
        c.rect(unterrichtszie_x, unterrichtszie_y - top_box_height, top_box_width, top_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label for first box
        c.setFont("Helvetica", 8)
        c.drawString(unterrichtszie_x + 2, unterrichtszie_y - top_box_height + 2, "Unterrichtsziel")
        
        # Second box: "von" - below first box
        von_x = unterrichtszie_x
        von_y = unterrichtszie_y - top_box_height - top_box_gap
        
        # Draw second box with light grey fill
        c.setFillColor(light_grey)
        c.rect(von_x, von_y - top_box_height, top_box_width, top_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label for second box
        c.setFont("Helvetica", 8)
        c.drawString(von_x + 2, von_y - top_box_height + 2, "von")
        
        # Third box: "bis" - right of second box
        bis_x = von_x + top_box_width + top_box_gap
        bis_y = von_y  # Same y position as second box
        
        # Draw third box with light grey fill
        c.setFillColor(light_grey)
        c.rect(bis_x, bis_y - top_box_height, top_box_width, top_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label for third box
        c.setFont("Helvetica", 8)
        c.drawString(bis_x + 2, bis_y - top_box_height + 2, "bis")
        
        # Fourth box: "Mitgliedsnummer" - at right margin, same height as "Unterrichtsziel"
        mitgliedsnummer_x = x + usable_width - top_box_width  # Right margin minus box width
        mitgliedsnummer_y = unterrichtszie_y  # Same height as "Unterrichtsziel"
        
        # Draw fourth box with light grey fill
        c.setFillColor(light_grey)
        c.rect(mitgliedsnummer_x, mitgliedsnummer_y - top_box_height, top_box_width, top_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label for fourth box
        c.setFont("Helvetica", 8)
        c.drawString(mitgliedsnummer_x + 2, mitgliedsnummer_y - top_box_height + 2, "Mitgliedsnummer")
        
        # Fifth box: "Zahlernummer" - below fourth box
        zahlernummer_x = mitgliedsnummer_x  # Same x position as fourth box
        zahlernummer_y = mitgliedsnummer_y - top_box_height - top_box_gap  # 1mm gap below
        
        # Draw fifth box with light grey fill
        c.setFillColor(light_grey)
        c.rect(zahlernummer_x, zahlernummer_y - top_box_height, top_box_width, top_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label for fifth box
        c.setFont("Helvetica", 8)
        c.drawString(zahlernummer_x + 2, zahlernummer_y - top_box_height + 2, "Zahlernummer")
        
        # Shift everything down by 2cm after subtitle
        y -= 2 * cm
        
        # Move down for section heading (increased space before)
        y -= 50
        
        # Section heading - bold, 12pt, underlined
        c.setFont("Helvetica-Bold", 12)
        section_text = "I. Mitgliedschaftsdaten"
        c.drawString(x, y, section_text)
        
        # Draw underline for section heading
        text_width = c.stringWidth(section_text, "Helvetica-Bold", 12)
        c.line(x, y - 2, x + text_width, y - 2)
        
        # Move down for the box (reduced space after)
        y -= 10
        
        # Draw the enlarged main box (now with bottom line to close it)
        c.setStrokeColor(black)
        c.setLineWidth(1)
        main_box_height = 235  # Enlarged by ~4mm (11 points)
        # Draw all four sides to close the box
        c.line(x, y, x + usable_width, y)  # Top line
        c.line(x, y, x, y - main_box_height)  # Left line
        c.line(x + usable_width, y, x + usable_width, y - main_box_height)  # Right line
        c.line(x, y - main_box_height, x + usable_width, y - main_box_height)  # Bottom line
        
        # Add gender selection text inside the box (top line)
        c.setFont("Helvetica", 10)
        c.setFillColor(black)
        
        # Get gender value from data
        sex = data_dict.get('sex', '')
        if sex is not None:
            sex = sex.lower()
        else:
            sex = ''
        
        # Create gender selection text with checkboxes
        gender_text = "Geschlecht: "
        
        # Position the text (right-aligned within the box)
        base_text = "Geschlecht: O weiblich / O männlich / O divers"
        text_width = c.stringWidth(base_text, "Helvetica", 10)
        c.drawRightString(x + usable_width - 10, y - 20, base_text)
        
        # Add checkmarks by overprinting "x" over "o" based on sex value
        if sex in ['weiblich', 'männlich', 'divers']:
            # Calculate positions for the "o" characters
            base_x = x + usable_width - 10 - text_width  # Starting position of the text
            
            # Position of each "o" in the text
            o_positions = []
            current_x = base_x
            for i, char in enumerate(base_text):
                if char == 'O':
                    o_positions.append(current_x)
                current_x += c.stringWidth(char, "Helvetica", 10)
            
            # Overprint "x" on the appropriate "o"
            if sex == 'weiblich' and len(o_positions) >= 1:
                c.drawString(o_positions[0], y - 20, "X")
            elif sex == 'männlich' and len(o_positions) >= 2:
                c.drawString(o_positions[1], y - 20, "X")
            elif sex == 'divers' and len(o_positions) >= 2:
                c.drawString(o_positions[2], y - 20, "X")
        
        # Position for the name and birth date boxes inside the main box (moved up more)
        inner_y = y - 40  # Move down inside the main box (reduced from 50 to 40)
        
        # Calculate inner box dimensions (slightly smaller to fit inside)
        inner_margin = 10  # Margin from main box edges
        inner_width = usable_width - (2 * inner_margin)
        inner_box_height = 1.2 * cm  # Slightly smaller height
        box_gap = 5  # Gap between boxes
        left_box_width = (inner_width * 2) / 3 - box_gap / 2
        right_box_width = inner_width / 3 - box_gap / 2
        
        # Draw the two adjacent boxes inside the main box with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + inner_margin, inner_y - inner_box_height, left_box_width, inner_box_height, fill=1)  # Left box
        c.rect(x + inner_margin + left_box_width + box_gap, inner_y - inner_box_height, right_box_width, inner_box_height, fill=1)  # Right box
        c.setFillColor(black)  # Reset to black for text
        
        # Add labels in 8pt font in lower left corner of each inner box
        c.setFont("Helvetica", 8)
        c.drawString(x + inner_margin + 2, inner_y - inner_box_height + 2, "Name, Vorname")
        c.drawString(x + inner_margin + left_box_width + box_gap + 2, inner_y - inner_box_height + 2, "geboren am")
        
        # Add content in 12pt font, left-aligned, baseline in middle of inner boxes
        c.setFont("Helvetica", 12)
        
        # Left box: last_name, first_name
        last_name = data_dict.get('last_name', '')
        first_name = data_dict.get('first_name', '')
        name_text = f"{last_name}, {first_name}" if last_name and first_name else f"{last_name}{first_name}"
        draw_text_in_box(name_text, x + inner_margin, inner_y - (inner_box_height / 2) - 4, left_box_width)
        
        # Right box: birth_date
        birth_date = data_dict.get('birth_date', '')
        draw_text_in_box(birth_date, x + inner_margin + left_box_width + box_gap, inner_y - (inner_box_height / 2) - 4, right_box_width)
        
        # Add another box below the name/birth date boxes
        discount_y = inner_y - inner_box_height - 10  # Position below the previous boxes with 10pt gap
        
        # Calculate dimensions for the discount box
        discount_box_height = 1.8 * cm  # Increased height from 1.2cm to 1.8cm
        discount_left_width = inner_width / 8  # Reduced from 1/6 to 1/8 of the width
        discount_right_width = inner_width - discount_left_width  # Rest of the width
        
        # Draw the discount box (no fill)
        c.rect(x + inner_margin, discount_y - discount_box_height, inner_width, discount_box_height)
        
        # Add content to the discount box
        c.setFont("Helvetica", 10)
        
        # Right column: Multi-line text
        right_text_line1 = "O ermäßigtes Mitglied, da bereits mind. 2 Mitglieder meines Haushaltes Mitglieder"
        right_text_line2 = "ohne Begrenzung der Mitgliedsdauer sind."
        right_text_line3 = "Diese sind"
        
        # Calculate text positioning for right column
        right_x = x + inner_margin + discount_left_width + 5
        line1_y = discount_y - (discount_box_height / 2) + 10  # Moved up by ~15pt
        line2_y = line1_y - 15  # 15pt gap between lines
        line3_y = line2_y - 15  # 15pt gap between lines
        
        # Left column: "als" - aligned with first line
        c.drawString(x + inner_margin + 5, line1_y, "als")
        
        c.drawString(right_x, line1_y, right_text_line1)
        c.drawString(right_x, line2_y, right_text_line2)
        c.drawString(right_x, line3_y, right_text_line3)
        
        # Add family member content in a box if defined
        family_member = data_dict.get('family_member', '')
        if family_member:
            # Calculate position for family member box
            family_box_x = right_x + c.stringWidth(right_text_line3, "Helvetica", 10) + 5
            family_box_width = (x + inner_margin + inner_width) - family_box_x - 5  # Fixed width extending to right edge minus 5
            family_box_height = 14  # Reduced height by 6pt (from 18 to 12)
            
            # Draw the box around family member text (shifted up 9pt total, extends above and below baseline)
            c.setFillColor(light_grey)
            c.rect(family_box_x, line3_y - 3, family_box_width, family_box_height, fill=1)
            c.setFillColor(black)  # Reset to black for text
            
            # Add family member text inside the box (same baseline as "Diese sind")
            draw_text_in_box(family_member, family_box_x, line3_y+1, family_box_width, padding=2)
        
        # Overprint "X" on "O" if discount is "ja"
        discount = data_dict.get('discount', '')
        if discount is not None:
            discount = discount.lower()
        else:
            discount = ''
        if discount == 'ja':
            # Calculate position of "O" in the first line (more precise)
            o_position = right_x
            c.drawString(o_position, line1_y, "X")
        
        # Add address row below the discount box
        address_y = discount_y - discount_box_height - 10  # Position below discount box with 10pt gap
        
        # Calculate dimensions for address boxes
        address_box_height = 1.2 * cm
        address_box_gap = 5  # Gap between address boxes
        address_box1_width = (inner_width * 0.6) - address_box_gap  # 60% of width minus gap
        address_box2_width = (inner_width * 0.15) - address_box_gap  # 15% of width minus gap
        address_box3_width = (inner_width * 0.25)  # 25% of width minus gap plus fixed amount
        
        # Draw the three address boxes with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + inner_margin, address_y - address_box_height, address_box1_width, address_box_height, fill=1)  # Street
        c.rect(x + inner_margin + address_box1_width + address_box_gap, address_y - address_box_height, address_box2_width, address_box_height, fill=1)  # ZIP
        c.rect(x + inner_margin + address_box1_width + address_box_gap + address_box2_width + address_box_gap, address_y - address_box_height, address_box3_width, address_box_height, fill=1)  # City
        c.setFillColor(black)  # Reset to black for text
        
        # Add labels in 8pt font in lower left corner of each box
        c.setFont("Helvetica", 8)
        c.drawString(x + inner_margin + 2, address_y - address_box_height + 2, "Straße, Hausnummer")
        c.drawString(x + inner_margin + address_box1_width + address_box_gap + 2, address_y - address_box_height + 2, "Postleitzahl")
        c.drawString(x + inner_margin + address_box1_width + address_box_gap + address_box2_width + address_box_gap + 2, address_y - address_box_height + 2, "Ort")
        
        # Add content in 12pt font, left-aligned, baseline in middle of boxes
        c.setFont("Helvetica", 12)
        
        # First box: street
        street = data_dict.get('street', '')
        draw_text_in_box(street, x + inner_margin, address_y - (address_box_height / 2) - 4, address_box1_width)
        
        # Second box: zip
        zip_code = data_dict.get('zip', '')
        draw_text_in_box(zip_code, x + inner_margin + address_box1_width + address_box_gap, address_y - (address_box_height / 2) - 4, address_box2_width)
        
        # Third box: city
        city = data_dict.get('city', '')
        draw_text_in_box(city, x + inner_margin + address_box1_width + address_box_gap + address_box2_width + address_box_gap, address_y - (address_box_height / 2) - 4, address_box3_width)
        
        # Add contact information row below the address boxes
        contact_y = address_y - address_box_height - 10  # Position below address boxes with 10pt gap
        
        # Calculate dimensions for contact boxes (email wider, phone smaller)
        contact_box_height = 1.2 * cm
        contact_box_gap = 5  # Gap between contact boxes
        base_contact_box_width = (inner_width / 3) - (2 * contact_box_gap / 3)  # Base 1/3 width minus gap
        
        # Adjust widths: email +1cm, phone -1cm from left
        email_box_width = base_contact_box_width + 1 * cm
        phone_box_width = base_contact_box_width - 1 * cm
        profession_box_width = base_contact_box_width  # Keep profession box unchanged
        
        # Draw the three contact boxes with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + inner_margin, contact_y - contact_box_height, email_box_width, contact_box_height, fill=1)  # Email
        c.rect(x + inner_margin + email_box_width + contact_box_gap, contact_y - contact_box_height, phone_box_width, contact_box_height, fill=1)  # Phone
        c.rect(x + inner_margin + email_box_width + contact_box_gap + phone_box_width + contact_box_gap, contact_y - contact_box_height, profession_box_width, contact_box_height, fill=1)  # Profession
        c.setFillColor(black)  # Reset to black for text
        
        # Add labels in 8pt font in lower left corner of each box
        c.setFont("Helvetica", 8)
        c.drawString(x + inner_margin + 2, contact_y - contact_box_height + 2, "E-Mail")
        c.drawString(x + inner_margin + email_box_width + contact_box_gap + 2, contact_y - contact_box_height + 2, "Telefon / Mobil")
        c.drawString(x + inner_margin + email_box_width + contact_box_gap + phone_box_width + contact_box_gap + 2, contact_y - contact_box_height + 2, "Beruf")
        
        # Add content in 12pt font, left-aligned, baseline in middle of boxes
        c.setFont("Helvetica", 12)
        
        # First box: email
        email = data_dict.get('email', '')
        draw_text_in_box(email, x + inner_margin, contact_y - (contact_box_height / 2) - 4, email_box_width)
        
        # Second box: phone
        phone = data_dict.get('phone', '')
        draw_text_in_box(phone, x + inner_margin + email_box_width + contact_box_gap, contact_y - (contact_box_height / 2) - 4, phone_box_width)
        
        # Third box: profession
        profession = data_dict.get('profession', '')
        draw_text_in_box(profession, x + inner_margin + email_box_width + contact_box_gap + phone_box_width + contact_box_gap, contact_y - (contact_box_height / 2) - 4, profession_box_width)
        
        # Start a new outer box for legal guardian information
        guardian_y = contact_y - contact_box_height - 30  # Position below contact boxes with 30pt gap (reduced from 50pt)
        
        # Calculate dimensions for the guardian box
        guardian_box_height = 160  # Enlarged height to accommodate all content and extend to bottom
        guardian_box_width = usable_width
        
        # Draw the guardian box
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(x, guardian_y - guardian_box_height, guardian_box_width, guardian_box_height)
        
        # Add the heading (without underline)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 10, guardian_y - 20, "Bei Minderjährigen: Angaben des gesetzlichen Vertreters:")
        
        # Add gender selection row (left-aligned, indented by 1.5cm)
        c.setFont("Helvetica", 10)
        c.setFillColor(black)
        
        # Get applicant gender value from data
        applicant_sex = data_dict.get('applicant_sex', '')
        if applicant_sex is not None:
            applicant_sex = applicant_sex.lower()
        else:
            applicant_sex = ''
        
        # Create gender selection text with checkboxes
        guardian_gender_text = "Geschlecht: O weiblich / O männlich / O divers"
        
        # Position the text (left-aligned, indented by 1.5cm)
        indent_x = x + 1.5 * cm
        c.drawString(indent_x, guardian_y - 45, guardian_gender_text)
        
        # Add checkmarks by overprinting "x" over "o" based on applicant_sex value
        if applicant_sex in ['weiblich', 'männlich', 'divers']:
            # Calculate positions for the "O" characters
            o_positions = []
            current_x = indent_x
            for i, char in enumerate(guardian_gender_text):
                if char == 'O':
                    o_positions.append(current_x)
                current_x += c.stringWidth(char, "Helvetica", 10)
            
            # Overprint "x" on the appropriate "O"
            if applicant_sex == 'weiblich' and len(o_positions) >= 1:
                c.drawString(o_positions[0], guardian_y - 45, "X")
            elif applicant_sex == 'männlich' and len(o_positions) >= 2:
                c.drawString(o_positions[1], guardian_y - 45, "X")
            elif applicant_sex == 'divers' and len(o_positions) >= 3:
                c.drawString(o_positions[2], guardian_y - 45, "X")
        
        # Add applicant name row (full width)
        applicant_name_y = guardian_y - 70  # Position below gender selection
        
        # Calculate dimensions for applicant name box
        applicant_name_box_height = 1.2 * cm
        applicant_name_box_width = guardian_box_width - 20  # Full width minus margins
        
        # Draw the applicant name box with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + 10, applicant_name_y - applicant_name_box_height, applicant_name_box_width, applicant_name_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label in 8pt font in lower left corner
        c.setFont("Helvetica", 8)
        c.drawString(x + 12, applicant_name_y - applicant_name_box_height + 2, "Name, Vorname (gesetzl. Vertreter)")
        
        # Add content in 12pt font, left-aligned, baseline in middle of box
        applicant_last_name = data_dict.get('applicant_last_name', '')
        applicant_first_name = data_dict.get('applicant_first_name', '')
        applicant_name_text = f"{applicant_last_name}, {applicant_first_name}" if applicant_last_name and applicant_first_name else f"{applicant_last_name}{applicant_first_name}"
        draw_text_in_box(applicant_name_text, x + 10, applicant_name_y - (applicant_name_box_height / 2) - 4, applicant_name_box_width, padding=5)
        
        # Add applicant address row (same layout as member address)
        applicant_address_y = applicant_name_y - applicant_name_box_height - 10  # Position below name box
        
        # Calculate dimensions for applicant address boxes
        applicant_address_box_height = 1.2 * cm
        applicant_address_box_gap = 5  # Gap between applicant address boxes
        applicant_address_box1_width = (applicant_name_box_width * 0.6) - applicant_address_box_gap  # 60% of width minus gap
        applicant_address_box2_width = (applicant_name_box_width * 0.15) - applicant_address_box_gap  # 15% of width minus gap
        applicant_address_box3_width = (applicant_name_box_width * 0.25)  # 25% of width minus gap plus fixed amount
        
        # Draw the three applicant address boxes with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + 10, applicant_address_y - applicant_address_box_height, applicant_address_box1_width, applicant_address_box_height, fill=1)  # Street
        c.rect(x + 10 + applicant_address_box1_width + applicant_address_box_gap, applicant_address_y - applicant_address_box_height, applicant_address_box2_width, applicant_address_box_height, fill=1)  # ZIP
        c.rect(x + 10 + applicant_address_box1_width + applicant_address_box_gap + applicant_address_box2_width + applicant_address_box_gap, applicant_address_y - applicant_address_box_height, applicant_address_box3_width, applicant_address_box_height, fill=1)  # City
        c.setFillColor(black)  # Reset to black for text
        
        # Add labels in 8pt font in lower left corner of each box
        c.setFont("Helvetica", 8)
        c.drawString(x + 12, applicant_address_y - applicant_address_box_height + 2, "Straße, Hausnummer (sofern abweichend vom Mitglied)")
        c.drawString(x + 12 + applicant_address_box1_width + applicant_address_box_gap, applicant_address_y - applicant_address_box_height + 2, "Postleitzahl")
        c.drawString(x + 12 + applicant_address_box1_width + applicant_address_box_gap + applicant_address_box2_width + applicant_address_box_gap, applicant_address_y - applicant_address_box_height + 2, "Ort")
        
        # Add content in 12pt font, left-aligned, baseline in middle of boxes
        c.setFont("Helvetica", 12)
        
        # First box: applicant_street
        applicant_street = data_dict.get('applicant_street', '')
        draw_text_in_box(applicant_street, x + 10, applicant_address_y - (applicant_address_box_height / 2) - 4, applicant_address_box1_width, padding=5)
        
        # Second box: applicant_zip
        applicant_zip = data_dict.get('applicant_zip', '')
        draw_text_in_box(applicant_zip, x + 10 + applicant_address_box1_width + applicant_address_box_gap, applicant_address_y - (applicant_address_box_height / 2) - 4, applicant_address_box2_width, padding=5)
        
        # Third box: applicant_city
        applicant_city = data_dict.get('applicant_city', '')
        draw_text_in_box(applicant_city, x + 10 + applicant_address_box1_width + applicant_address_box_gap + applicant_address_box2_width + applicant_address_box_gap, applicant_address_y - (applicant_address_box_height / 2) - 4, applicant_address_box3_width, padding=5)
        
        # Add section header for SEPA mandate
        sepa_y = applicant_address_y - applicant_address_box_height - 50  # Position below guardian box with 50pt gap (increased from 30pt)
        
        # Section heading - bold, 12pt, underlined (same as first header)
        c.setFont("Helvetica-Bold", 12)
        sepa_section_text = "II. Erteilung eines SEPA-Lastschriftmandats:"
        c.drawString(x, sepa_y, sepa_section_text)
        
        # Draw underline for section heading
        sepa_text_width = c.stringWidth(sepa_section_text, "Helvetica-Bold", 12)
        c.line(x, sepa_y - 2, x + sepa_text_width, sepa_y - 2)
        
        # Start the SEPA mandate box
        sepa_box_y = sepa_y - 15  # Position below section header (reduced from 30pt)
        
        # Calculate dimensions for the SEPA box
        sepa_box_height = 120  # Enlarged height to properly enclose inner fields
        sepa_box_width = usable_width
        
        # Draw the SEPA box
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(x, sepa_box_y - sepa_box_height, sepa_box_width, sepa_box_height)
        
        # First row: Account holder (full width)
        account_holder_y = sepa_box_y - 20  # Position inside the box
        
        # Calculate dimensions for account holder box
        account_holder_box_height = 1.2 * cm
        account_holder_box_width = inner_width  # Use same width as other sections
        
        # Draw the account holder box with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + inner_margin, account_holder_y - account_holder_box_height, account_holder_box_width, account_holder_box_height, fill=1)
        c.setFillColor(black)  # Reset to black for text
        
        # Add label in 8pt font in lower left corner
        c.setFont("Helvetica", 8)
        c.drawString(x + inner_margin + 2, account_holder_y - account_holder_box_height + 2, "Name des Kontoinhabers")
        
        # Add content in 12pt font, left-aligned, baseline in middle of box
        account_holder = data_dict.get('account_holder', '')
        draw_text_in_box(account_holder, x + inner_margin, account_holder_y - (account_holder_box_height / 2) - 4, account_holder_box_width)
        
        # Second row: IBAN and BIC (2/3 and 1/3 width)
        iban_bic_y = account_holder_y - account_holder_box_height - 10  # Position below account holder box
        
        # Calculate dimensions for IBAN and BIC boxes
        iban_bic_box_height = 1.2 * cm
        iban_bic_gap = 5  # Gap between IBAN and BIC boxes
        iban_box_width = (account_holder_box_width * 2) / 3 - iban_bic_gap / 2  # 2/3 of width minus gap
        bic_box_width = account_holder_box_width / 3 - iban_bic_gap / 2  # 1/3 of width minus gap
        
        # Draw the IBAN and BIC boxes with light grey fill
        c.setFillColor(light_grey)
        c.rect(x + 10, iban_bic_y - iban_bic_box_height, iban_box_width, iban_bic_box_height, fill=1)  # IBAN
        c.rect(x + 10 + iban_box_width + iban_bic_gap, iban_bic_y - iban_bic_box_height, bic_box_width, iban_bic_box_height, fill=1)  # BIC
        c.setFillColor(black)  # Reset to black for text
        
        # Add labels in 8pt font in lower left corner of each box
        c.setFont("Helvetica", 8)
        c.drawString(x + 12, iban_bic_y - iban_bic_box_height + 2, "IBAN")
        c.drawString(x + 12 + iban_box_width + iban_bic_gap, iban_bic_y - iban_bic_box_height + 2, "BIC")
        
        # Add content in 12pt font, left-aligned, baseline in middle of boxes
        c.setFont("Helvetica", 12)
        
        # IBAN box with formatting
        iban = data_dict.get('iban', '')
        if iban:
            # Format IBAN in groups of 4 characters with spaces
            formatted_iban = ' '.join([iban[i:i+4] for i in range(0, len(iban), 4)])
            draw_text_in_box(formatted_iban, x + 10, iban_bic_y - (iban_bic_box_height / 2) - 4, iban_box_width, padding=5)
        
        # BIC box
        bic = data_dict.get('bic', '')
        draw_text_in_box(bic, x + 10 + iban_box_width + iban_bic_gap, iban_bic_y - (iban_bic_box_height / 2) - 4, bic_box_width, padding=5)
        
    except Exception as e:
        raise Exception(f"Error creating PDF page: {e}")


def convert(csv_path: str, pdf_path: str) -> None:
    """
    Read a CSV file and convert all rows to a multi-page PDF.
    
    Args:
        csv_path (str): Path to the input CSV file
        pdf_path (str): Path where the output PDF should be saved
        
    Raises:
        Exception: If there's an error reading the CSV or creating the PDF
    """
    try:
        # Read the CSV file
        data_list = read_csv_to_dicts_with_validation(csv_path)
        
        if not data_list:
            raise Exception("CSV file contains no data rows")
        
        # Create canvas for multi-page PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        
        # Process each row
        for i, row in enumerate(data_list):
            # Generate PDF page for this row
            generate_pdf_from_dict(row, c)
            
            # Add a new page if this isn't the last row
            if i < len(data_list) - 1:
                c.showPage()
        
        # Save the PDF
        c.save()
        
        print(f"✅ Successfully converted {len(data_list)} rows from '{csv_path}' to '{pdf_path}'")
        
    except Exception as e:
        raise Exception(f"Error in conversion process: {e}")



def read_csv_to_dicts_with_validation(filename: str) -> List[Dict[str, Any]]:
    """
    Read a CSV file with Windows 1252 encoding and semicolon separators,
    with additional validation and error handling.
    
    Args:
        filename (str): Path to the CSV file to read
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries, each representing a row
                              with column headers as keys
                              
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        UnicodeDecodeError: If the file cannot be decoded with Windows 1252 encoding
        ValueError: If the CSV file is empty or has no headers
        Exception: For other CSV parsing errors
    """
    try:
        with open(filename, 'r', encoding='windows-1252', newline='') as csvfile:
            # Read the first line to check if file has content
            first_line = csvfile.readline().strip()
            if not first_line:
                raise ValueError(f"File '{filename}' is empty")
            
            # Reset file pointer to beginning
            csvfile.seek(0)
            
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Check if headers exist
            if not reader.fieldnames:
                raise ValueError(f"File '{filename}' has no headers")
            
            # Convert to list and validate
            data = list(reader)
            
            # Check if we have any data rows
            if not data:
                print(f"Warning: File '{filename}' contains only headers, no data rows")
            
            # Convert the data using the key mapping for all rows
            for i, row in enumerate(data):
                converted_row = {}
                for original_key, mapped_key in key_mapping.items():
                    if mapped_key is not None:
                        converted_row[mapped_key] = row.get(original_key, '')
                data[i] = converted_row
            
            return data
            
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Failed to decode file '{filename}' with Windows 1252 encoding: {e}")
    except Exception as e:
        raise Exception(f"Error reading CSV file '{filename}': {e}")


def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) != 3:
        print("Usage: python csv_converter.py <input_csv_path> <output_pdf_path>")
        print("Example: python csv_converter.py enrollments.csv output.pdf")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    pdf_path = sys.argv[2]
    
    try:
        convert(csv_path, pdf_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()