"""
Tests for API routes
"""


def test_health_check(client):
    """Test health check endpoint."""
    resp = client.get('/api/health')
    
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    
    data = resp.get_json()
    assert data['status'] == 'healthy'


def test_version_endpoint(client):
    """Test version endpoint."""
    resp = client.get('/api/version')
    
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    
    data = resp.get_json()
    assert 'version' in data
    assert data['version'] == '1.0.0'
