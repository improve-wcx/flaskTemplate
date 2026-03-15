"""
Pytest configuration and shared fixtures
"""
import os
import sys
import pytest
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set test environment
os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture
def app():
    """Create application for testing."""
    import tempfile
    from app import create_app
    
    # Create temp directory for logs
    tmp_dir = tempfile.mkdtemp()
    log_dir = os.path.join(tmp_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up temp log files BEFORE creating app
    from utils import logger as logger_module
    logger_module.LOG_DIR = log_dir
    logger_module.LOG_FILE = os.path.join(log_dir, 'app.log')
    logger_module.LOG_TRACE_FILE = os.path.join(log_dir, 'trace.log')
    
    # Create the log files immediately
    open(logger_module.LOG_FILE, 'a', encoding='utf-8').close()
    open(logger_module.LOG_TRACE_FILE, 'a', encoding='utf-8').close()
    
    # Create app with testing config
    app = create_app('testing')
    app.config['TESTING'] = True
    
    yield app
    
    # Cleanup disabled to allow log inspection
    # import shutil
    # try:
    #     shutil.rmtree(tmp_dir)
    # except:
    #     pass


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner."""
    return app.test_cli_runner()
