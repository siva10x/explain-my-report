# from flask import Blueprint, request, jsonify
# from services.file_parser import parse_file
# from services.langchain_service import explain_medical_text
# from utils.helpers import validate_request
# import logging

# explain_bp = Blueprint('explain', __name__)

# @explain_bp.route('/explain', methods=['POST'])
# def explain_report():
#     try:
#         # Validate request
#         validation_error = validate_request(request)
#         if validation_error:
#             return jsonify({'error': validation_error}), 400
            
#         # Process input
#         text = ''
#         if 'file' in request.files:
#             text = parse_file(request.files['file'])
#         elif request.form.get('text'):  # Handle text input from UI form
#             text = request.form['text']
#         elif request.is_json:
#             data = request.get_json()
#             text = data.get('text', '')
#         else:
#             return jsonify({'error': 'Invalid input format. Use file upload, form data with "text" field, or JSON with "text" field.'}), 400
            
#         if not text.strip():
#             return jsonify({'error': 'No text content found'}), 400
            
#         # Get explanations
#         explanations = explain_medical_text(text)
        
#         logging.info('Successfully processed text input')
#         return jsonify({'explanations': explanations}), 200
        
#     except Exception as e:
#         logging.error(f'Error processing request: {str(e)}')
#         return jsonify({'error': 'Internal server error'}), 500


from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from services.file_parser import parse_file
from services.langchain_service import explain_medical_text
from utils.helpers import validate_request, debug_request
import logging

explain_bp = Blueprint('explain', __name__)

@explain_bp.route('/explain/prescription', methods=['POST', 'OPTIONS'])
@cross_origin()
def explain_prescription():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    print("Received prescription request")
    debug_request(request)  # Debug the incoming request
    try:
        # Validate request
        validation_error = validate_request(request)
        if validation_error:
            return jsonify({'error': validation_error}), 400
            
        # Process input
        text = ''
        if 'file' in request.files:
            text = parse_file(request.files['file'])
        elif request.form.get('text'):
            text = request.form['text']
        elif request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            return jsonify({'error': 'Invalid input format. Use file upload, form data with "text" field, or JSON with "text" field.'}), 400
            
        if not text.strip():
            return jsonify({'error': 'No text content found'}), 400
            
        # Get explanations with prescription-specific prompt
        explanations = explain_medical_text(text, prompt_type='prescription')
        
        logging.info('Successfully processed prescription input')
        return jsonify({'explanations': explanations}), 200
        
    except Exception as e:
        logging.error(f'Error processing prescription request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@explain_bp.route('/explain/diagnosis', methods=['POST', 'OPTIONS'])
@cross_origin()
def explain_diagnosis():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    debug_request(request)  # Debug the incoming request
    try:
        # Validate request
        validation_error = validate_request(request)
        if validation_error:
            return jsonify({'error': validation_error}), 400
            
        # Process input
        text = ''
        if 'file' in request.files:
            text = parse_file(request.files['file'])
        elif request.form.get('text'):
            text = request.form['text']
        elif request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            return jsonify({'error': 'Invalid input format. Use file upload, form data with "text" field, or JSON with "text" field.'}), 400
            
        if not text.strip():
            return jsonify({'error': 'No text content found'}), 400
            
        # Get explanations with diagnosis-specific prompt
        explanations = explain_medical_text(text, prompt_type='diagnosis')
        
        logging.info('Successfully processed diagnosis input')
        return jsonify({'explanations': explanations}), 200
        
    except Exception as e:
        logging.error(f'Error processing diagnosis request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@explain_bp.route('/explain/query', methods=['POST', 'OPTIONS'])
@cross_origin()
def explain_query():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    debug_request(request)  # Debug the incoming request
    try:
        # Validate request
        validation_error = validate_request(request)
        if validation_error:
            return jsonify({'error': validation_error}), 400
            
        # Process input
        text = ''
        if 'file' in request.files:
            text = parse_file(request.files['file'])
        elif request.form.get('text'):
            text = request.form['text']
        elif request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            return jsonify({'error': 'Invalid input format. Use file upload, form data with "text" field, or JSON with "text" field.'}), 400
            
        if not text.strip():
            return jsonify({'error': 'No text content found'}), 400
            
        # Get explanations with query-specific prompt
        explanations = explain_medical_text(text, prompt_type='query')
        
        logging.info('Successfully processed general query input')
        return jsonify({'explanations': explanations}), 200
        
    except Exception as e:
        logging.error(f'Error processing query request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500