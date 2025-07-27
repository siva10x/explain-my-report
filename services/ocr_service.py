import pytesseract
from pdf2image import convert_from_bytes
import re

def extract_text_from_image(image):
    """Extract text from an image using pytesseract."""
    try:
        text = pytesseract.image_to_string(image, config='--psm 6')  # Use PSM 6 for better table handling
        return clean_text(text)
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")

def extract_text_from_pdf(file_content):
    """Extract text from PDF by converting to images."""
    print("Extracting text from PDF")
    try:
        images = convert_from_bytes(file_content)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image, config='--psm 6') + '\n'
        return clean_text(text)
    except Exception as e:
        raise Exception(f"PDF processing failed: {str(e)}")

def clean_text(text):
    """Remove common headers, footers, and extra whitespace, and improve table structure."""
    # Remove multiple newlines and extra spaces
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Basic header/footer removal
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'Confidential|Report Generated.*$', '', text)
    
    # Try to preserve table-like structure by splitting on repeated patterns
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if any(keyword in line.lower() for keyword in ['medicine', 'dosage', 'duration', 'tab', 'cap']):
            cleaned_lines.append(line)
        elif not line or any(keyword in line.lower() for keyword in ['dr.', 'clinic', 'near', 'mob', 'reg']):
            continue  # Skip doctor details and irrelevant lines
    return '\n'.join(cleaned_lines)