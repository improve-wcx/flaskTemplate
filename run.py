"""
Application entry point.

Usage:
    python run.py
"""
from app import create_app

# Create app with default configuration (development)
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
