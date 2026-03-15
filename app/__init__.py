"""
Flask application factory.

Usage:
    from app import app
    app.run()
    
Or with run.py:
    python run.py
"""
import os
from flask import Flask
from utils.logger import setup_logger
from config import get_config


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration name ('development', 'testing', 'production')
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Load configuration from JSON
    config = get_config(config_name)
    
    # Create Flask app
    app = Flask(__name__)
    
    # Apply configuration
    app_config = config.get('app', {})
    app.debug = app_config.get('debug', False)
    app.testing = app_config.get('testing', False)
    
    # Security settings
    security = config.get('security', {})
    app.secret_key = security.get('secret_key', 'dev-secret-key')
    
    # Session settings
    session_config = config.get('session', {})
    from datetime import timedelta
    app.permanent_session_lifetime = timedelta(
        hours=session_config.get('permanent_session_lifetime_hours', 1)
    )
    
    # Cookie settings
    app.config.update(
        SESSION_COOKIE_SECURE=security.get('session_cookie_secure', False),
        SESSION_COOKIE_HTTPONLY=security.get('session_cookie_httponly', True),
        SESSION_COOKIE_SAMESITE=security.get('session_cookie_samesite', 'Lax')
    )
    
    # Initialize logger with config
    logging_config = config.get('logging', {})
    import utils.logger as logger_module
    logger_module.LOG_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        logging_config.get('log_dir', 'logs')
    )
    logger_module.LOG_FILE = os.path.join(
        logger_module.LOG_DIR, 
        logging_config.get('app_log_file', 'app.log')
    )
    logger_module.LOG_TRACE_FILE = os.path.join(
        logger_module.LOG_DIR, 
        logging_config.get('trace_log_file', 'trace.log')
    )
    
    logger = setup_logger("projectTemplate", level=getattr(
        __import__('logging'), 
        logging_config.get('level', 'DEBUG').upper()
    ))
    app.logger = logger
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    # from app.routes.admin import admin_bp  # Uncomment when needed
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    # app.register_blueprint(admin_bp)  # Uncomment when needed
    
    # Before request hook
    @app.before_request
    def log_request():
        from flask import request
        logger.info("%s %s", request.method, request.path)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return "Not Found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return "Internal Server Error", 500
    
    return app


# For backward compatibility
app = create_app()
