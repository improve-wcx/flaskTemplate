"""
Base configuration settings
"""
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration with common settings."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Security
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Timeouts
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    
    # Database (future)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        """Initialize app with this config."""
        pass


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    
    # Security (relaxed for testing)
    SESSION_COOKIE_SECURE = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Logging
    LOG_LEVEL = 'INFO'


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
