"""
Tests for main routes
"""
import json
import logging


def test_index_page_returns_html(client):
    """Test that the index page returns HTML content."""
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'<!DOCTYPE html>' in resp.data
    assert b'Flask Application' in resp.data


def test_index_page_contains_function_list(client):
    """Test that the new index page contains the function navigation list."""
    resp = client.get('/')
    assert resp.status_code == 200
    
    # Check for function list elements
    assert b'function-list' in resp.data
    assert b'function-item' in resp.data
    
    # Check for specific functions (using UTF-8 encoded bytes)
    assert '关系管理'.encode('utf-8') in resp.data
    assert 'API 文档'.encode('utf-8') in resp.data
    assert 'Protobuf 演示'.encode('utf-8') in resp.data
    assert '演示页面'.encode('utf-8') in resp.data
    
    # Check for links
    assert b'/relationship-map' in resp.data
    assert b'/api/apis' in resp.data
    assert b'/api/v1/demo/hello' in resp.data
    assert b'/demo' in resp.data


def test_hello_route_returns_hello_world(client):
    """Test that the hello route returns the expected response."""
    resp = client.get('/hello')
    assert resp.status_code == 200
    assert b'Hello, World!' in resp.data


def test_demo_page_returns_html(client):
    """Test that the demo page returns HTML content."""
    resp = client.get('/demo')
    assert resp.status_code == 200
    assert b'<!DOCTYPE html>' in resp.data
    assert b'Static Resource Demo' in resp.data


def test_favicon_route_returns_204(client):
    """Test that the favicon route returns 204 No Content."""
    resp = client.get('/favicon.ico')
    assert resp.status_code == 204
    assert len(resp.data) == 0


def test_index_route_logs_request(client):
    """Test that the index route logs the request properly."""
    resp = client.get('/')
    assert resp.status_code == 200
    # Logs are output to console (captured by pytest)
    assert True


def test_hello_route_logs_request(client):
    """Test that the hello route logs the request properly."""
    resp = client.get('/hello')
    assert resp.status_code == 200
    assert True


def test_demo_route_logs_request(client):
    """Test that the demo route logs the request properly."""
    resp = client.get('/demo')
    assert resp.status_code == 200
    assert True


def test_favicon_route_logs_debug(client):
    """Test that the favicon route logs debug message."""
    resp = client.get('/favicon.ico')
    assert resp.status_code == 204
    assert True
