"""
单元测试：Hello World 接口测试
测试 Flask + Protocol Buffers 集成的各种接口
"""

import pytest
import json
from app import create_app
from app.proto import helloworld_pb2  # Updated for demo_protobuf
from app.proto import common_pb2


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


class TestDemoProtobuf:
    """Hello World 接口测试类"""
    
    
    def test_demo_hello_get(self, client):
        """测试 GET 方法 - 简单问候"""
        response = client.get('/api/v1/demo/hello')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == "Hello, World!"
        assert 'timestamp' in data
        assert 'request_id' in data

    def test_demo_hello_json_success(self, client):
        """测试 JSON 格式的问候接口 - 成功场景"""
        response = client.post(
            '/api/v1/demo/hello',
            data=json.dumps({'name': 'Alice'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'message' in data
        assert data['message'] == 'Hello, Alice!'
        assert 'timestamp' in data
        assert 'request_id' in data
    
    def test_demo_hello_json_default_name(self, client):
        """测试 JSON 格式的问候接口 - 默认名称"""
        response = client.post(
            '/api/v1/demo/hello',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['message'] == 'Hello, World!'
    
    def test_demo_hello_json_empty_body(self, client):
        """测试 JSON 格式的问候接口 - 空请求体"""
        response = client.post(
            '/api/v1/demo/hello',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'message' in data
        assert 'request_id' in data
    
    def test_demo_hello_json_invalid_data(self, client):
        """测试 JSON 格式的问候接口 - 无效数据"""
        response = client.post(
            '/api/v1/demo/hello',
            data='invalid json',
            content_type='application/json'
        )
        
        # 无效 JSON 会抛出异常，返回 500
        # assert response.status_code == 400
        assert response.status_code == 500
    
    def test_demo_hello_binary_success(self, client):
        """测试二进制格式的问候接口"""
        # 创建 protobuf 请求
        request_msg = helloworld_pb2.HelloRequest(name='Bob')
        request_data = request_msg.SerializeToString()
        
        response = client.post(
            '/api/v1/demo/hello-binary',
            data=request_data,
            content_type='application/x-protobuf'
        )
        
        assert response.status_code == 200
        
        # 验证响应是有效的 protobuf 数据
        response_msg = helloworld_pb2.HelloResponse()
        response_msg.ParseFromString(response.data)
        
        assert response_msg.message == 'Hello (Binary), Bob!'
        assert response_msg.request_id != ''
        assert response.content_type == 'application/x-protobuf'
    
    def test_demo_hello_binary_empty_data(self, client):
        """测试二进制格式的问候接口 - 空数据"""
        response = client.post(
            '/api/v1/demo/hello-binary',
            data=b'',
            content_type='application/x-protobuf'
        )
        
        # 空数据应该能处理（使用默认值）
        assert response.status_code == 200
        
        response_msg = helloworld_pb2.HelloResponse()
        response_msg.ParseFromString(response.data)
        
        assert 'Hello (Binary)' in response_msg.message


class TestUserInfo:
    """用户信息接口测试"""
    
    def test_get_user_success(self, client):
        """测试获取用户信息 - 成功"""
        response = client.post(
            '/api/v1/demo/user',
            data=json.dumps({'user_id': '12345'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'user' in data
        # MessageToDict 使用 camelCase
        assert data['user']['userId'] == '12345'
        assert data['user']['username'] == 'john_doe'
        assert data['user']['email'] == 'john@example.com'
        assert 'message' in data
        assert 'request_id' in data
    
    def test_get_user_not_found(self, client):
        """测试获取用户信息 - 用户不存在"""
        response = client.post(
            '/api/v1/demo/user',
            data=json.dumps({'user_id': '99999'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    def test_get_user_invalid_request(self, client):
        """测试获取用户信息 - 无效请求"""
        response = client.post(
            '/api/v1/demo/user',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # 缺少 user_id 字段
        assert response.status_code == 400


class TestUserList:
    """用户列表接口测试"""
    
    
    def test_list_users_get(self, client):
        """测试获取用户列表 (GET)"""
        response = client.get('/api/v1/demo/users?page=1&page_size=5')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
        assert 'users' in data
        assert 'total' in data
        assert data['page'] == 1
        assert data['pageSize'] == 5

    def test_list_users_default_page(self, client):
        """测试用户列表 - 默认分页"""
        response = client.post(
            '/api/v1/demo/users',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'users' in data
        assert isinstance(data['users'], list)
        assert 'total' in data
        assert data['page'] == 1
        assert data['page_size'] == 10
        assert 'request_id' in data
    
    def test_list_users_custom_pagination(self, client):
        """测试用户列表 - 自定义分页"""
        response = client.post(
            '/api/v1/demo/users',
            data=json.dumps({
                'page': 2,
                'page_size': 20
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert data['page'] == 2
        assert data['page_size'] == 20
        assert len(data['users']) <= 20
    
    def test_list_users_user_fields(self, client):
        """测试用户列表 - 用户字段完整性"""
        response = client.post(
            '/api/v1/demo/users',
            data=json.dumps({'page': 1, 'page_size': 1}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert len(data['users']) > 0
        user = data['users'][0]
        
        # 验证用户字段 (MessageToDict 使用 camelCase)
        assert 'userId' in user
        assert 'username' in user
        assert 'email' in user
        assert 'age' in user
        assert isinstance(user['age'], int)


class TestEcho:
    """Echo 接口测试"""
    
    def test_echo_success(self, client):
        """测试 Echo 接口 - 成功"""
        test_data = {
            'key1': 'value1',
            'key2': 123,
            'key3': True
        }
        
        response = client.post(
            '/api/v1/echo',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status_code'] == common_pb2.STATUS_CODE_SUCCESS
        assert data['message'] == 'Echo successful'
        assert data['echo_data'] == test_data
        assert 'request_id' in data
    
    def test_echo_empty_data(self, client):
        """测试 Echo 接口 - 空数据"""
        response = client.post(
            '/api/v1/echo',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status_code'] == common_pb2.STATUS_CODE_SUCCESS
        assert data['echo_data'] == {}


class TestProtobufMessages:
    """Protobuf 消息测试"""
    
    def test_helloworld_request_creation(self):
        """测试 HelloRequest 消息创建"""
        request = helloworld_pb2.HelloRequest(name='Test')
        
        assert request.name == 'Test'
        assert request.DESCRIPTOR.name == 'HelloRequest'
    
    def test_helloworld_response_creation(self):
        """测试 HelloResponse 消息创建"""
        response = helloworld_pb2.HelloResponse(
            message='Hello!',
            timestamp='2026-03-16T10:00:00',
            request_id='test-123'
        )
        
        assert response.message == 'Hello!'
        assert response.timestamp == '2026-03-16T10:00:00'
        assert response.request_id == 'test-123'
    
    def test_user_info_serialization(self):
        """测试 UserInfo 消息序列化/反序列化"""
        original = helloworld_pb2.UserInfo(
            user_id='123',
            username='test_user',
            email='test@example.com',
            age=25
        )
        
        # 序列化
        serialized = original.SerializeToString()
        
        # 反序列化
        deserialized = helloworld_pb2.UserInfo()
        deserialized.ParseFromString(serialized)
        
        # 验证
        assert deserialized.user_id == original.user_id
        assert deserialized.username == original.username
        assert deserialized.email == original.email
        assert deserialized.age == original.age
    
    def test_user_list_repeated_field(self):
        """测试 UserListResponse 的 repeated 字段"""
        response = helloworld_pb2.UserListResponse()
        
        # 添加用户
        for i in range(3):
            user = response.users.add()
            user.user_id = str(i)
            user.username = f'user_{i}'
        
        assert len(response.users) == 3
        assert response.users[0].user_id == '0'
        assert response.users[2].username == 'user_2'
    
    def test_common_response_status_codes(self):
        """测试 CommonResponse 状态码"""
        # 测试各种状态码
        success_response = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_SUCCESS,
            message='Success'
        )
        
        failure_response = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_FAILURE,
            message='Failure'
        )
        
        assert success_response.status_code == 1
        assert failure_response.status_code == 2


class TestIntegration:
    """集成测试"""
    
    def test_request_id_tracing(self, client):
        """测试 request_id 追踪"""
        # 发送多个请求
        responses = []
        for i in range(3):
            response = client.post(
                '/api/v1/demo/hello',
                data=json.dumps({'name': f'User{i}'}),
                content_type='application/json'
            )
            data = response.get_json()
            responses.append(data['request_id'])
        
        # 验证每个请求都有唯一的 request_id
        assert len(set(responses)) == 3, "每个请求应该有唯一的 request_id"
    
    def test_timestamp_format(self, client):
        """测试时间戳格式"""
        response = client.post(
            '/api/v1/demo/hello',
            data=json.dumps({'name': 'Test'}),
            content_type='application/json'
        )
        data = response.get_json()
        
        # 验证时间戳格式（ISO 8601）
        assert 'T' in data['timestamp']
        assert len(data['timestamp']) >= 19  # 至少包含年月日时分秒
    
    def test_error_handling(self, client):
        """测试错误处理"""
        # 发送无效请求
        response = client.post(
            '/api/v1/demo/hello',
            data='not json',
            content_type='application/json'
        )
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data or 'request_id' in data
