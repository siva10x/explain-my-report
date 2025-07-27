# from flask import Flask
# from routes.explain import explain_bp
# from dotenv import load_dotenv
# import logging
# import os

# # Load environment variables
# load_dotenv()

# def create_app():
#     app = Flask(__name__)
    
#     # Ensure logs directory exists
#     log_dir = 'logs'
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
    
#     # Configure logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s %(levelname)s: %(message)s'
#     )
    
#     # Get the root logger and clear existing handlers
#     logger = logging.getLogger()
#     logger.handlers.clear()  # Clear all existing handlers to prevent duplicates
    
#     # Create file handler for logging to file
#     file_handler = logging.FileHandler('logs/app.log')
#     file_handler.setLevel(logging.INFO)
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    
#     # Create stream handler for logging to console
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(logging.INFO)
#     stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    
#     # Add handlers to the root logger
#     logger.addHandler(file_handler)
#     logger.addHandler(stream_handler)
    
#     # Configure app
#     app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 5MB limit
#     app.config['UPLOAD_FOLDER'] = 'uploads'
#     app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    
#     # Ensure uploads directory exists
#     upload_dir = 'uploads'
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)
    
#     # Register blueprints
#     app.register_blueprint(explain_bp, url_prefix='/api')
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, host='0.0.0.0', port=5001)


from flask import Flask, render_template
from routes.explain import explain_bp
from dotenv import load_dotenv
import logging
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Ensure logs directory exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    
    # Get the root logger and clear existing handlers
    logger = logging.getLogger()
    logger.handlers.clear()
    
    # Create file handler for logging to file
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    
    # Create stream handler for logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    
    # Add handlers to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    # Configure app
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    
    # Ensure uploads directory exists
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Register blueprints
    app.register_blueprint(explain_bp, url_prefix='/api')
    
    # Add route for UI (optional, remove if not needed)
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)