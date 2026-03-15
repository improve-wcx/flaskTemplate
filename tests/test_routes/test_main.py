"""
Tests for main routes
"""
import json
import logging


def test_hello_route_returns_hello_world(client):
    """Test that the hello route returns the expected response."""
    resp = client.get('/')
    
    assert resp.status_code == 200
    assert b'Hello, World!' in resp.data


def test_favicon_route_returns_204(client):
    """Test that the favicon route returns 204 No Content."""
    resp = client.get('/favicon.ico')
    
    assert resp.status_code == 204
    assert len(resp.data) == 0


def test_hello_route_logs_request(client):
    """Test that the hello route logs the request properly."""
    resp = client.get('/')
    assert resp.status_code == 200
    
    # Verify logs were written (check that log files exist)
    from utils import logger as logger_module
    import os
    
    assert os.path.exists(logger_module.LOG_FILE), "Log file should exist"
    
    with open(logger_module.LOG_FILE, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    
    # Find INFO entry for GET /
    info_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == 'INFO' and 'GET /' in json.loads(line)[5]
    ]
    
    assert len(info_entries) >= 1, "Should have logged the GET / request"


def test_hello_route_logs_debug(client):
    """Test that the hello route logs debug message."""
    resp = client.get('/')
    assert resp.status_code == 200
    
    from utils import logger as logger_module
    
    with open(logger_module.LOG_FILE, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    
    debug_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == 'DEBUG' and 'handling hello route' in json.loads(line)[5]
    ]
    
    assert len(debug_entries) >= 1, "Should have logged 'handling hello route'"


def test_favicon_route_logs_debug(client):
    """Test that the favicon route logs debug message."""
    resp = client.get('/favicon.ico')
    assert resp.status_code == 204
    
    from utils import logger as logger_module
    
    with open(logger_module.LOG_FILE, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    
    debug_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == 'DEBUG' and 'handling favicon route' in json.loads(line)[5]
    ]
    
    assert len(debug_entries) >= 1, "Should have logged 'handling favicon route'"
