from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from services.file_parser import parse_file
from services.langchain_service import explain_medical_text
from utils.helpers import validate_request, debug_request
import logging

# Create namespace for API documentation
api = Namespace('explain', description='Medical text explanation operations')

# Define models for Swagger documentation
text_input_model = api.model('TextInput', {
    'text': fields.String(required=True, description='Medical text to explain')
})

explanation_response_model = api.model('ExplanationResponse', {
    'explanations': fields.Raw(description='Medical explanations'),
    'success': fields.Boolean(description='Request success status')
})

error_response_model = api.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

# File upload parser
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, 
                          help='Medical document file (PDF, JPG, PNG, TXT, DOCX)')

# Text input parser
text_parser = api.parser()
text_parser.add_argument('text', location='form', required=True, 
                        help='Medical text to explain')

@api.route('/prescription')
class PrescriptionExplanation(Resource):
    @api.doc('explain_prescription')
    @api.expect(upload_parser)
    @api.marshal_with(explanation_response_model, code=200)
    @api.marshal_with(error_response_model, code=400)
    @api.marshal_with(error_response_model, code=500)
    def post(self):
        """Explain prescription document or text"""
        debug_request(request)
        try:
            # Validate request
            validation_error = validate_request(request)
            if validation_error:
                return {'error': validation_error}, 400
                
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
                return {'error': 'Invalid input format'}, 400
                
            if not text.strip():
                return {'error': 'No text content found'}, 400
                
            # Get explanations with prescription-specific prompt
            explanations = explain_medical_text(text, prompt_type='prescription')
            
            logging.info('Successfully processed prescription input')
            return {'explanations': explanations, 'success': True}, 200
            
        except Exception as e:
            logging.error(f'Error processing prescription request: {str(e)}')
            return {'error': 'Internal server error'}, 500

    def options(self):
        """Handle preflight OPTIONS request"""
        return {'message': 'OK'}, 200

@api.route('/diagnosis')
class DiagnosisExplanation(Resource):
    @api.doc('explain_diagnosis')
    @api.expect(upload_parser)
    @api.marshal_with(explanation_response_model, code=200)
    @api.marshal_with(error_response_model, code=400)
    @api.marshal_with(error_response_model, code=500)
    def post(self):
        """Explain diagnosis document or text"""
        debug_request(request)
        try:
            # Validate request
            validation_error = validate_request(request)
            if validation_error:
                return {'error': validation_error}, 400
                
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
                return {'error': 'Invalid input format'}, 400
                
            if not text.strip():
                return {'error': 'No text content found'}, 400
                
            # Get explanations with diagnosis-specific prompt
            explanations = explain_medical_text(text, prompt_type='diagnosis')
            
            logging.info('Successfully processed diagnosis input')
            return {'explanations': explanations, 'success': True}, 200
            
        except Exception as e:
            logging.error(f'Error processing diagnosis request: {str(e)}')
            return {'error': 'Internal server error'}, 500

    def options(self):
        """Handle preflight OPTIONS request"""
        return {'message': 'OK'}, 200

@api.route('/query')
class QueryExplanation(Resource):
    @api.doc('explain_query')
    @api.expect(text_input_model)
    @api.marshal_with(explanation_response_model, code=200)
    @api.marshal_with(error_response_model, code=400)
    @api.marshal_with(error_response_model, code=500)
    def post(self):
        """Explain general medical query"""
        debug_request(request)
        try:
            # Validate request
            validation_error = validate_request(request)
            if validation_error:
                return {'error': validation_error}, 400
                
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
                return {'error': 'Invalid input format'}, 400
                
            if not text.strip():
                return {'error': 'No text content found'}, 400
                
            # Get explanations with general prompt
            explanations = explain_medical_text(text, prompt_type='general')
            
            logging.info('Successfully processed query input')
            return {'explanations': explanations, 'success': True}, 200
            
        except Exception as e:
            logging.error(f'Error processing query request: {str(e)}')
            return {'error': 'Internal server error'}, 500

    def options(self):
        """Handle preflight OPTIONS request"""
        return {'message': 'OK'}, 200
