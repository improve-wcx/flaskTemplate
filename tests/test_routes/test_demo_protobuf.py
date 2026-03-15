""" Protocol Buffers 演示接口单元测试 """
import json
import pytest
from app.proto import demo_pb2, common_pb2


@pytest.fixture
def client():
    from app import create_app
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestDemoProtobuf:
    """GET 方法测试"""
    
    def test_hello_get(self, client):
        """测试 GET /hello - 简单问候"""
        response = client.get('/api/v1/demo/hello')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Hello, World!"
        assert 'timestamp' in data
        assert 'requestId' in data


class TestDemoProtobufPost:
    """POST 方法测试"""
    
    def test_hello_post(self, client):
        """测试 POST /hello - 带参数问候"""
        response = client.post(
            '/api/v1/demo/hello',
            data=json.dumps({"name": "Alice"}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Hello, Alice!"
        assert 'requestId' in data
        
    def test_user_get(self, client):
        """测试 GET /user/<id> - 获取用户"""
        response = client.get('/api/v1/demo/user/12345')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['userId'] == '12345'
        assert 'username' in data['user']
    
    def test_user_get_not_found(self, client):
        """测试 GET /user/<id> - 用户不存在"""
        response = client.get('/api/v1/demo/user/99999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
    
    def test_users_post(self, client):
        """测试 POST /users - 用户列表"""
        response = client.post(
            '/api/v1/demo/users',
            data=json.dumps({"page": 1, "page_size": 3}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['users']) == 3
        assert data['total'] == 100
        assert 'userId' in data['users'][0]
    
    def test_hello_request(self):
        """测试 HelloRequest 创建"""
        req = demo_pb2.HelloRequest(name="Test")
        assert req.name == "Test"
    
    def test_hello_response(self):
        """测试 HelloResponse 创建"""
        resp = demo_pb2.HelloResponse(
            message="Hello!",
            timestamp="2026-03-16T10:00:00",
            request_id="test-id"
        )
        assert resp.message == "Hello!"
    
    def test_common_response(self):
        """测试 CommonResponse 状态码"""
        resp = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_SUCCESS,
            message="Success",
            request_id="test"
        )
        assert resp.status_code == common_pb2.STATUS_CODE_SUCCESS


class TestIntegration:
    """集成测试"""
    
    def test_request_id_tracing(self, client):
        """测试 Request ID 追踪"""
        response1 = client.get('/api/v1/demo/hello')
        response2 = client.get('/api/v1/demo/hello')
        
        id1 = response1.get_json()['requestId']
        id2 = response2.get_json()['requestId']
        
        assert id1 != id2  # 不同请求应有不同 ID
    
    def test_timestamp_format(self, client):
        """测试时间戳格式"""
        response = client.get('/api/v1/demo/hello')
        data = response.get_json()
        
        # 检查 ISO 8601 格式
        assert 'T' in data['timestamp']
        assert len(data['timestamp']) >= 19
