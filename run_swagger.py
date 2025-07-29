#!/usr/bin/env python3
"""
Simple script to start the Flask app with Swagger documentation
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Flask app with Swagger documentation...")
    print("📚 Swagger UI available at: http://localhost:5001/swagger/")
    print("🔗 API endpoints available at: http://localhost:5001/api/explain/")
    print("🏠 Main app available at: http://localhost:5001/")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
