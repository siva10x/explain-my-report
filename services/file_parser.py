from services.ocr_service import extract_text_from_image, extract_text_from_pdf
from docx import Document
import magic
from PIL import Image
import io

def parse_file(file):
    """Parse uploaded file based on its MIME type."""
    print("parsing file")
    mime = magic.Magic(mime=True)
    file_content = file.read()
    mime_type = mime.from_buffer(file_content)
    
    if mime_type in ['image/jpeg', 'image/png']:
        image = Image.open(io.BytesIO(file_content))
        return extract_text_from_image(image)
        
    elif mime_type == 'application/pdf':
        print("parsing pdf")
        return extract_text_from_pdf(file_content)
        
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = Document(io.BytesIO(file_content))
        return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
        
    elif mime_type == 'text/plain':
        return file_content.decode('utf-8')
        
    else:
        raise ValueError('Unsupported file type')
