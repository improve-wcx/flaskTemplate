"""
WSGI entry point for production servers (e.g., gunicorn).

Usage with gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
from app import create_app

app = create_app('production')
