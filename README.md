# Explain My Report API

A Flask-based REST API that simplifies medical reports using OCR and AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Install from https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`

3. Copy `.env.example` to `.env` and add your OpenAI API key.

4. Run the application:
```bash
python app.py
```

## Testing

Test with file upload:
```bash
curl -X POST http://localhost:5000/api/explain \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_report.pdf"
```

Test with text input:
```bash
curl -X POST http://localhost:5000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"text": "HbA1c: 8.5%\nRx: Metformin 500mg BD"}'
```

## Project Structure

- `app.py`: Main Flask application
- `routes/`: API endpoints
- `services/`: Business logic for OCR, file parsing, and AI processing
- `utils/`: Helper functions
- `logs/`: Application logs
```