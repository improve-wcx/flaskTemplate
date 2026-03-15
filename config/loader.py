"""
JSON-based configuration loader.

Usage:
    from config.loader import load_config
    config = load_config('development')
    host = config['app']['host']
"""
import json
import os
from typing import Dict, Any, Optional
from datetime import timedelta


class ConfigLoader:
    """Load configuration from JSON file."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to config.json. If None, uses default path.
        """
        if config_path is None:
            # Default path: config.json in the same directory as this file
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        self.config_path = config_path
        self._config_data: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """
        Load all configurations from JSON file.
        
        Returns:
            Dictionary containing all environment configurations.
        """
        if self._config_data is None:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        
        return self._config_data
    
    def get_config(self, env_name: str = 'development') -> Dict[str, Any]:
        """
        Get configuration for a specific environment.
        
        Args:
            env_name: Environment name ('development', 'testing', 'production')
            
        Returns:
            Configuration dictionary for the specified environment.
            
        Raises:
            KeyError: If environment not found.
            ValueError: If config file is invalid.
        """
        config_data = self.load()
        
        if env_name not in config_data:
            available = ', '.join(config_data.keys())
            raise KeyError(f"Environment '{env_name}' not found. Available: {available}")
        
        return config_data[env_name]
    
    def get_value(
        self, 
        env_name: str, 
        key_path: str, 
        default: Any = None
    ) -> Any:
        """
        Get a specific configuration value using dot notation.
        
        Args:
            env_name: Environment name
            key_path: Dot-separated path (e.g., 'app.host', 'logging.level')
            default: Default value if key not found
            
        Returns:
            Configuration value or default.
        """
        config = self.get_config(env_name)
        keys = key_path.split('.')
        
        value = config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value


# Global loader instance
_loader = ConfigLoader()


def load_config(env_name: str = 'development') -> Dict[str, Any]:
    """
    Load configuration for an environment.
    
    Args:
        env_name: Environment name
        
    Returns:
        Configuration dictionary
    """
    return _loader.get_config(env_name)


def get_config_value(
    env_name: str, 
    key_path: str, 
    default: Any = None
) -> Any:
    """
    Get a specific configuration value.
    
    Args:
        env_name: Environment name
        key_path: Dot-separated key path
        default: Default value
        
    Returns:
        Configuration value
    """
    return _loader.get_value(env_name, key_path, default)


def reload_config() -> None:
    """Reload configuration from file (useful for testing)."""
    global _loader
    _loader = ConfigLoader()
    _loader._config_data = None  # Clear cached data
