"""
Tests for JSON configuration system.
"""
import os
import json
import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory with test config files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"
        
        # Create test config
        test_config = {
            "development": {
                "app": {
                    "host": "127.0.0.1",
                    "port": 5000,
                    "debug": True
                },
                "logging": {
                    "level": "DEBUG",
                    "log_dir": "logs"
                }
            },
            "testing": {
                "app": {
                    "host": "localhost",
                    "port": 5001,
                    "debug": True,
                    "testing": True
                },
                "logging": {
                    "level": "WARNING"
                }
            },
            "production": {
                "app": {
                    "host": "0.0.0.0",
                    "port": 8080,
                    "debug": False
                },
                "logging": {
                    "level": "INFO"
                }
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(test_config, f)
        
        yield str(config_path)


def test_load_config_success(temp_config_dir):
    """Test successful loading of configuration."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    config = loader.load()
    
    assert 'development' in config
    assert 'testing' in config
    assert 'production' in config
    assert config['development']['app']['port'] == 5000


def test_get_config_development(temp_config_dir):
    """Test getting development configuration."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    config = loader.get_config('development')
    
    assert config['app']['host'] == '127.0.0.1'
    assert config['app']['port'] == 5000
    assert config['app']['debug'] is True


def test_get_config_testing(temp_config_dir):
    """Test getting testing configuration."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    config = loader.get_config('testing')
    
    assert config['app']['port'] == 5001
    assert config['logging']['level'] == 'WARNING'


def test_get_config_production(temp_config_dir):
    """Test getting production configuration."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    config = loader.get_config('production')
    
    assert config['app']['host'] == '0.0.0.0'
    assert config['app']['port'] == 8080
    assert config['app']['debug'] is False


def test_get_config_invalid_env(temp_config_dir):
    """Test getting configuration for invalid environment."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    
    with pytest.raises(KeyError, match="Environment 'invalid' not found"):
        loader.get_config('invalid')


def test_get_value_with_dot_notation(temp_config_dir):
    """Test getting value using dot notation."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    
    # Test nested value
    host = loader.get_value('development', 'app.host')
    assert host == '127.0.0.1'
    
    # Test another nested value
    level = loader.get_value('testing', 'logging.level')
    assert level == 'WARNING'


def test_get_value_with_default(temp_config_dir):
    """Test getting value with default when key doesn't exist."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    
    # Non-existent key should return default
    value = loader.get_value('development', 'app.nonexistent', 'default_value')
    assert value == 'default_value'


def test_get_value_nonexistent_env(temp_config_dir):
    """Test getting value from non-existent environment."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader(temp_config_dir)
    
    with pytest.raises(KeyError):
        loader.get_value('nonexistent', 'app.host')


def test_config_file_not_found():
    """Test error when config file doesn't exist."""
    from config.loader import ConfigLoader
    
    loader = ConfigLoader('/nonexistent/path/config.json')
    
    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_config_function(temp_config_dir):
    """Test the load_config convenience function."""
    import sys
    sys.path.insert(0, os.path.dirname(temp_config_dir))
    
    # Temporarily modify the loader path
    from config import loader
    original_loader = loader._loader
    loader._loader = loader.ConfigLoader(temp_config_dir)
    
    try:
        config = loader.load_config('development')
        assert config['app']['port'] == 5000
    finally:
        loader._loader = original_loader


def test_get_config_value_function(temp_config_dir):
    """Test the get_config_value convenience function."""
    import sys
    sys.path.insert(0, os.path.dirname(temp_config_dir))
    
    from config import loader
    original_loader = loader._loader
    loader._loader = loader.ConfigLoader(temp_config_dir)
    
    try:
        port = loader.get_config_value('production', 'app.port')
        assert port == 8080
        
        # Test with default
        missing = loader.get_config_value('production', 'app.missing', 9999)
        assert missing == 9999
    finally:
        loader._loader = original_loader


def test_reload_config(temp_config_dir):
    """Test reloading configuration."""
    import sys
    sys.path.insert(0, os.path.dirname(temp_config_dir))
    
    from config import loader
    
    # Create a new loader with the temp config
    test_loader = loader.ConfigLoader(temp_config_dir)
    
    # Load initial config
    config1 = test_loader.get_config('development')
    assert config1['app']['port'] == 5000
    
    # Modify config file
    with open(temp_config_dir, 'r') as f:
        config_data = json.load(f)
    
    config_data['development']['app']['port'] = 9999
    
    with open(temp_config_dir, 'w') as f:
        json.dump(config_data, f)
    
    # Reload by creating new loader instance
    test_loader._config_data = None  # Clear cache
    config2 = test_loader.get_config('development')
    assert config2['app']['port'] == 9999
