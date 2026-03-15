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
    
    # Import configurations
    from config.base import config_map
    config_class = config_map.get(config_name, config_map['default'])
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize logger
    logger = setup_logger("projectTemplate")
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
    
    # Error handlers (optional, can be moved to error handlers module)
    @app.errorhandler(404)
    def not_found(error):
        return "Not Found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return "Internal Server Error", 500
    
    return app


# For backward compatibility
app = create_app()
