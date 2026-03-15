""" Flask application factory.
Usage: from app import app
app.run()
Or with run.py: python run.py
"""
import os
from flask import Flask
from utils.logger import setup_logger
from config import get_config

def create_app(config_name=None):
    """ Application factory function.
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
    def before_request():
        """Set up request_id for tracing and log the request."""
        from flask import request, g
        from utils.logger import set_request_id
        
        # Generate and set request_id for this request
        request_id = set_request_id()
        
        # Store in Flask's g object for access in routes
        g.request_id = request_id
        
        # Log the incoming request with request_id
        logger.info("%s %s", request.method, request.path, extra={'request_id': request_id})
    
    # After request hook
    @app.after_request
    def after_request(response):
        """Log the response with request_id."""
        from flask import request, g
        from utils.logger import get_request_id
        
        # Get request_id from g or context
        request_id = getattr(g, 'request_id', None) or get_request_id()
        
        # Log response with request_id
        logger.info(
            "%s %s %d %s",
            request.method,
            request.path,
            response.status_code,
            request.remote_addr,
            extra={'request_id': request_id}
        )
        
        return response
    
    # Return the app instance
    return app
