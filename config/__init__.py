"""
Configuration package.

Provides JSON-based configuration loading for different environments.

Usage:
    from config import get_config
    config = get_config('development')
    host = config['app']['host']
"""
from .loader import load_config, get_config_value, reload_config


def get_config(env_name: str = None):
    """
    Get configuration for current environment.

    Args:
        env_name: Environment name. If None, uses FLASK_ENV env var or 'development'

    Returns:
        Configuration dictionary
    """
    if env_name is None:
        import os
        env_name = os.environ.get('FLASK_ENV', 'development')

    return load_config(env_name)


__all__ = ['get_config', 'load_config', 'get_config_value', 'reload_config']
