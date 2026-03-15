"""
Application entry point.

Usage:
    python run.py
"""
import os
from app import create_app
from config import get_config

# Create app with default configuration (development)
app = create_app()

if __name__ == '__main__':
    # Get host and port from configuration
    env = os.environ.get('FLASK_ENV', 'development')
    config = get_config(env)
    app_config = config.get('app', {})
    
    host = app_config.get('host', '127.0.0.1')
    port = app_config.get('port', 5000)
    debug = app_config.get('debug', True)
    
    app.run(host=host, port=port, debug=debug)
