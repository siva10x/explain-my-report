from flask import request
import logging

def validate_request(req):
    """Validate incoming request."""
    # Check if file is uploaded
    if 'file' in req.files and req.files['file'].filename != '':
        file = req.files['file']
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'docx'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return 'Invalid file type'
        return None  # Valid file upload
    
    # Check if JSON data with text
    elif req.is_json:
        data = req.get_json()
        if not data or not data.get('text') or not data.get('text').strip():
            return 'Text field is required'
        return None  # Valid JSON input
    
    # Check if form data with text
    elif req.form.get('text'):
        if not req.form['text'].strip():
            return 'Text field is required'
        return None  # Valid form text input
    
    # No valid input found
    else:
        return 'Invalid request format. Please provide either a file upload or text content.'

def debug_request(req):
    """Debug helper to log request details."""
    logging.info(f"Request method: {req.method}")
    logging.info(f"Content type: {req.content_type}")
    logging.info(f"Has files: {'file' in req.files}")
    if 'file' in req.files:
        file = req.files['file']
        logging.info(f"File name: {file.filename}")
        logging.info(f"File content type: {file.content_type}")
    logging.info(f"Is JSON: {req.is_json}")
    logging.info(f"Form data: {dict(req.form)}")
    logging.info(f"Files: {list(req.files.keys())}")