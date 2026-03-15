""" Protocol Buffers 演示接口

简单示例：展示如何在 Flask 中使用 Protocol Buffers 进行数据序列化。

接口设计：
- GET: 获取资源
- POST: 创建/处理资源
- 每个方法只保留一个典型接口，便于理解
"""

from flask import Blueprint, request, jsonify
from app.proto import helloworld_pb2, common_pb2
from google.protobuf.json_format import ParseDict, MessageToDict
import uuid
from datetime import datetime

# 创建蓝图
demo_protobuf_bp = Blueprint('demo_protobuf', __name__, url_prefix='/api/v1/demo')


def generate_request_id():
    """生成请求 ID"""
    return str(uuid.uuid4())


@demo_protobuf_bp.route('/hello', methods=['GET'])
def hello_get():
    """
    GET 示例：简单问候
    
    请求：GET /api/v1/demo/hello
    
    响应:
    {
        "message": "Hello, World!",
        "timestamp": "2026-03-16T10:00:00",
        "request_id": "uuid"
    }
    """
    request_id = generate_request_id()
    
    response_msg = helloworld_pb2.HelloResponse(
        message="Hello, World!",
        timestamp=datetime.now().isoformat(),
        request_id=request_id
    )
    
    return jsonify(MessageToDict(response_msg)), 200


@demo_protobuf_bp.route('/hello', methods=['POST'])
def hello_post():
    """
    POST 示例：带参数的问候
    
    请求体 (JSON):
    {
        "name": "Alice"
    }
    
    响应:
    {
        "message": "Hello, Alice!",
        "timestamp": "2026-03-16T10:00:00",
        "request_id": "uuid"
    }
    """
    request_id = generate_request_id()
    
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Invalid JSON", "request_id": request_id}), 400
        
        # JSON -> Protobuf
        request_msg = helloworld_pb2.HelloRequest()
        ParseDict(json_data, request_msg)
        
        name = request_msg.name if request_msg.name else "World"
        
        response_msg = helloworld_pb2.HelloResponse(
            message=f"Hello, {name}!",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        return jsonify(MessageToDict(response_msg)), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "request_id": request_id}), 500


@demo_protobuf_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET 示例：获取用户信息 (RESTful)
    
    请求：GET /api/v1/demo/user/12345
    
    响应:
    {
        "success": true,
        "user": {
            "userId": "12345",
            "username": "john_doe",
            "email": "john@example.com",
            "age": 25
        },
        "message": "User found",
        "request_id": "uuid"
    }
    """
    request_id = generate_request_id()
    
    try:
        # 模拟用户数据
        mock_users = {
            "12345": {
                "user_id": "12345",
                "username": "john_doe",
                "email": "john@example.com",
                "age": 25
            }
        }
        
        if user_id not in mock_users:
            return jsonify({
                "success": False,
                "message": f"User {user_id} not found",
                "request_id": request_id
            }), 404
        
        user_data = mock_users[user_id]
        
        response_msg = helloworld_pb2.UserInfoResponse(
            success=True,
            request_id=request_id,
            message="User found"
        )
        
        response_msg.user.user_id = user_data["user_id"]
        response_msg.user.username = user_data["username"]
        response_msg.user.email = user_data["email"]
        response_msg.user.age = user_data["age"]
        
        return jsonify({
            "success": response_msg.success,
            "user": MessageToDict(response_msg.user),
            "message": response_msg.message,
            "request_id": response_msg.request_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "request_id": request_id}), 500


@demo_protobuf_bp.route('/users', methods=['POST'])
def list_users():
    """
    POST 示例：获取用户列表 (展示 repeated 字段)
    
    请求体 (JSON):
    {
        "page": 1,
        "page_size": 10
    }
    
    响应:
    {
        "success": true,
        "users": [
            {"userId": "1", "username": "user1", ...},
            {"userId": "2", "username": "user2", ...}
        ],
        "total": 100,
        "page": 1,
        "pageSize": 10,
        "request_id": "uuid"
    }
    """
    request_id = generate_request_id()
    
    try:
        json_data = request.get_json() or {}
        
        request_msg = helloworld_pb2.UserListRequest()
        ParseDict(json_data, request_msg)
        
        page = request_msg.page if request_msg.page else 1
        page_size = request_msg.page_size if request_msg.page_size else 10
        
        # 生成模拟用户
        total_users = 100
        users = []
        for i in range(page_size):
            user_id = str((page - 1) * page_size + i + 1)
            if int(user_id) > total_users:
                break
            users.append({
                "user_id": user_id,
                "username": f"user_{user_id}",
                "email": f"user{user_id}@example.com",
                "age": 20 + (int(user_id) % 50)
            })
        
        response_msg = helloworld_pb2.UserListResponse(
            success=True,
            total=total_users,
            page=page,
            page_size=page_size,
            request_id=request_id
        )
        
        for user_data in users:
            user_msg = response_msg.users.add()
            user_msg.user_id = user_data["user_id"]
            user_msg.username = user_data["username"]
            user_msg.email = user_data["email"]
            user_msg.age = user_data["age"]
        
        return jsonify({
            "success": response_msg.success,
            "users": [MessageToDict(u) for u in response_msg.users],
            "total": response_msg.total,
            "page": response_msg.page,
            "pageSize": response_msg.page_size,
            "request_id": response_msg.request_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "request_id": request_id}), 500


@demo_protobuf_bp.route('/echo', methods=['POST'])
def echo():
    """
    POST 示例：Echo 接口 (展示通用响应格式)
    
    请求体 (JSON): 任意数据
    {
        "key": "value"
    }
    
    响应:
    {
        "statusCode": 0,
        "message": "Success",
        "request_id": "uuid",
        "echo_data": {"key": "value"}
    }
    """
    request_id = generate_request_id()
    
    try:
        json_data = request.get_json() or {}
        
        response_msg = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_SUCCESS,
            message="Echo successful",
            request_id=request_id
        )
        
        return jsonify({
            "statusCode": response_msg.status_code,
            "message": response_msg.message,
            "request_id": response_msg.request_id,
            "echo_data": json_data
        }), 200
        
    except Exception as e:
        response_msg = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_FAILURE,
            message=str(e),
            request_id=request_id
        )
        return jsonify({
            "statusCode": response_msg.status_code,
            "message": response_msg.message,
            "request_id": response_msg.request_id
        }), 500
