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


def test_list_apis(client):
    """Test list all APIs endpoint."""
    resp = client.get('/api/apis')
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    data = resp.get_json()
    
    # 验证返回结构
    assert 'total' in data
    assert 'apis' in data
    assert 'request_id' in data
    
    # 验证总数
    assert data['total'] > 0
    
    # 验证 apis 是字典
    assert isinstance(data['apis'], dict)
    
    # 验证至少包含几个分类
    assert '系统' in data['apis']
    assert 'Protobuf 演示' in data['apis']


def test_list_apis_contains_health(client):
    """Test /apis returns /api/health."""
    resp = client.get('/api/apis')
    data = resp.get_json()
    
    system_apis = data['apis'].get('系统', [])
    health_api = next((api for api in system_apis if api['path'] == '/api/health'), None)
    
    assert health_api is not None
    assert health_api['method'] == 'GET'
    assert health_api['description'] == '健康检查'


def test_list_apis_contains_demo_apis(client):
    """Test /apis returns Protobuf demo APIs."""
    resp = client.get('/api/apis')
    data = resp.get_json()
    
    demo_apis = data['apis'].get('Protobuf 演示', [])
    assert len(demo_apis) > 0
    
    # 验证包含 hello 接口
    hello_apis = [api for api in demo_apis if 'hello' in api['path']]
    assert len(hello_apis) > 0


def test_list_apis_format(client):
    """Test /apis return format."""
    resp = client.get('/api/apis')
    assert resp.status_code == 200
    
    data = resp.get_json()
    
    # 验证 total 与实际接口数一致
    total_count = sum(len(apis) for apis in data['apis'].values())
    assert data['total'] == total_count
