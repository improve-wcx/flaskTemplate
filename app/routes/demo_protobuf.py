"""
Flask + Protocol Buffers 集成示例
展示如何在 Flask Web 接口中使用 protobuf 进行数据序列化/反序列化
"""

from flask import Blueprint, request, jsonify
from app.proto import helloworld_pb2
from app.proto import common_pb2
from google.protobuf.json_format import ParseDict, MessageToDict
import uuid
import time
from datetime import datetime

# 创建蓝图
demo_protobuf_bp = Blueprint('demo_protobuf', __name__, url_prefix='/api/v1/demo')


def generate_request_id():
    """生成请求 ID"""
    return str(uuid.uuid4())


@demo_protobuf_bp.route('/hello', methods=['GET', 'POST'])
def hello():
    """
    Hello World 接口示例
    
    GET 方法: 简单问候，无需参数
    POST 方法: 带参数的问候
    
    GET 请求:
    /api/v1/demo/hello
    
    POST 请求体 (JSON):
    {
        "name": "John"
    }
    
    响应体 (JSON):
    {
        "message": "Hello, John!",
        "timestamp": "2026-03-16T10:00:00",
        "request_id": "uuid-here"
    }
    """
    request_id = generate_request_id()
    
    try:
        # GET 方法：简单问候
        if request.method == 'GET':
            response_msg = helloworld_pb2.HelloResponse(
                message="Hello, World!",
                timestamp=datetime.now().isoformat(),
                request_id=request_id
            )
            return jsonify({
                "message": response_msg.message,
                "timestamp": response_msg.timestamp,
                "request_id": response_msg.request_id
            }), 200
        
        # POST 方法：带参数的问候
        json_data = request.get_json()
        if json_data is None:
            return jsonify({
                "error": "Invalid JSON data",
                "request_id": request_id
            }), 400
        
        # 2. 将 JSON 数据转换为 protobuf 消息
        request_msg = helloworld_pb2.HelloRequest()
        ParseDict(json_data, request_msg)
        
        # 3. 处理业务逻辑
        name = request_msg.name if request_msg.name else "World"
        
        # 4. 创建响应消息
        response_msg = helloworld_pb2.HelloResponse(
            message=f"Hello, {name}!",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        # 5. 返回 JSON 响应
        return jsonify({
            "message": response_msg.message,
            "timestamp": response_msg.timestamp,
            "request_id": response_msg.request_id
        }), 200
        
    except Exception as e:
        # 错误处理
        return jsonify({
            "error": str(e),
            "request_id": request_id
        }), 500


@demo_protobuf_bp.route('/hello-binary', methods=['POST'])
def hello_binary():
    """
    二进制数据接口示例 (展示 protobuf 的序列化能力)
    
    请求体 (Protobuf 二进制):
    HelloRequest 消息的二进制格式
    
    响应体 (Protobuf 二进制):
    HelloResponse 消息的二进制格式
    """
    try:
        # 1. 获取原始二进制数据
        raw_data = request.get_data()
        
        # 2. 反序列化 protobuf 消息
        request_msg = helloworld_pb2.HelloRequest()
        request_msg.ParseFromString(raw_data)
        
        # 3. 处理业务逻辑
        name = request_msg.name if request_msg.name else "World"
        request_id = generate_request_id()
        
        # 4. 创建响应消息
        response_msg = helloworld_pb2.HelloResponse(
            message=f"Hello (Binary), {name}!",
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
        # 5. 序列化为二进制并返回
        #    注意：设置 Content-Type 为 application/x-protobuf
        return response_msg.SerializeToString(), 200, {
            'Content-Type': 'application/x-protobuf'
        }
        
    except Exception as e:
        return str(e), 400


@demo_protobuf_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    获取单个用户信息 (RESTful GET)
    
    GET 请求:
    /api/v1/demo/user/12345
    
    响应体 (JSON):
    {
        "success": true,
        "user": {
            "userId": "12345",
            "username": "john_doe",
            "email": "john@example.com",
            "age": 25
        },
        "message": "User found",
        "request_id": "uuid-here"
    }
    """
    request_id = generate_request_id()
    
    try:
        # 1. 创建请求消息
        request_msg = helloworld_pb2.GetUserRequest(user_id=user_id)
        
        # 2. 模拟查询数据库
        
        # 模拟用户数据
        mock_users = {
            "12345": {
                "user_id": "12345",
                "username": "john_doe",
                "email": "john@example.com",
                "age": 25
            },
            "67890": {
                "user_id": "67890",
                "username": "jane_smith",
                "email": "jane@example.com",
                "age": 30
            }
        }
        
        if user_id not in mock_users:
            return jsonify({
                "success": False,
                "message": f"User {user_id} not found",
                "request_id": request_id
            }), 404
        
        # 3. 创建响应
        user_data = mock_users[user_id]
        response_msg = helloworld_pb2.UserInfoResponse(
            success=True,
            request_id=request_id,
            message="User found"
        )
        # 设置用户信息
        response_msg.user.user_id = user_data["user_id"]
        response_msg.user.username = user_data["username"]
        response_msg.user.email = user_data["email"]
        response_msg.user.age = user_data["age"]
        
        # 5. 转换为字典并返回
        return jsonify({
            "success": response_msg.success,
            "user": MessageToDict(response_msg.user),
            "message": response_msg.message,
            "request_id": response_msg.request_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "request_id": generate_request_id()
        }), 500


@demo_protobuf_bp.route('/users', methods=['GET', 'POST'])
def list_users():
    """
    用户列表接口示例 (展示 repeated 字段)
    
    GET 方法：通过查询参数分页
    POST 方法：通过请求体分页
    
    GET 请求:
    /api/v1/demo/users?page=1&page_size=10
    
    POST 请求体 (JSON):
    {
        "page": 1,
        "page_size": 10
    }
    
    响应体 (JSON):
    {
        "success": true,
        "users": [
            {"userId": "1", "username": "user1", ...},
            {"userId": "2", "username": "user2", ...}
        ],
        "total": 100,
        "page": 1,
        "pageSize": 10,
        "request_id": "uuid-here"
    }
    """
    request_id = generate_request_id()
    
    try:
        # GET 方法：从查询参数获取
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            page_size = request.args.get('page_size', 10, type=int)
            json_data = {"page": page, "page_size": page_size}
        else:
            # POST 方法：从请求体获取
            json_data = request.get_json()
            if json_data is None:
                json_data = {}
        
        # 2. 解析请求
        request_msg = helloworld_pb2.UserListRequest()
        ParseDict(json_data, request_msg)
        
        page = request_msg.page if request_msg.page else 1
        page_size = request_msg.page_size if request_msg.page_size else 10
        
        # 3. 模拟查询数据库
        total_users = 100
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_users)
        
        # 生成模拟用户列表
        users = []
        for i in range(start_idx, end_idx):
            user_id = str(i + 1)
            users.append({
                "user_id": user_id,
                "username": f"user_{user_id}",
                "email": f"user{user_id}@example.com",
                "age": 20 + (i % 50)
            })
        
        # 4. 创建响应
        response_msg = helloworld_pb2.UserListResponse(
            success=True,
            total=total_users,
            page=page,
            page_size=page_size,
            request_id=request_id
        )
        
        # 添加用户到 repeated 字段
        for user_data in users:
            user_msg = response_msg.users.add()
            user_msg.user_id = user_data["user_id"]
            user_msg.username = user_data["username"]
            user_msg.email = user_data["email"]
            user_msg.age = user_data["age"]
        
        # 5. 转换为字典并返回
        users_list = [MessageToDict(user) for user in response_msg.users]
        
        return jsonify({
            "success": response_msg.success,
            "users": users_list,
            "total": response_msg.total,
            "page": response_msg.page,
            "page_size": response_msg.page_size,
            "request_id": response_msg.request_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "request_id": generate_request_id()
        }), 500


@demo_protobuf_bp.route('/echo', methods=['POST'])
def echo():
    """
    Echo 接口示例 (展示通用响应格式)
    
    请求体 (JSON): 任意 JSON 数据
    
    响应体 (JSON):
    {
        "status_code": 1,
        "message": "Success",
        "request_id": "uuid-here"
    }
    """
    try:
        json_data = request.get_json()
        request_id = generate_request_id()
        
        # 创建通用响应
        response_msg = common_pb2.CommonResponse(
            status_code=common_pb2.STATUS_CODE_SUCCESS,
            message="Echo successful",
            request_id=request_id
        )
        
        return jsonify({
            "status_code": response_msg.status_code,
            "message": response_msg.message,
            "request_id": response_msg.request_id,
            "echo_data": json_data  # 返回原始数据
        }), 200
        
    except Exception as e:
        request_id = generate_request_id()
        return jsonify({
            "status_code": common_pb2.STATUS_CODE_FAILURE,
            "message": str(e),
            "request_id": request_id
        }), 500


# 使用示例说明
"""
在 Flask 中使用 Protocol Buffers 的步骤：

1. 定义 proto 文件 (proto/helloworld.proto)
   - 定义请求和响应消息结构
   - 运行代码生成脚本生成 Python 代码

2. 在 Flask 路由中处理请求：
   a) 获取 JSON 数据: json_data = request.get_json()
   b) 转换为 protobuf 消息: msg.FromDict(json_data)
   c) 处理业务逻辑
   d) 创建响应消息
   e) 转换为字典：msg.ToDict() 或手动转换
   f) 返回 JSON 响应

3. 或者使用二进制格式：
   a) 获取原始数据: raw_data = request.get_data()
   b) 反序列化: msg.ParseFromString(raw_data)
   c) 处理业务逻辑
   d) 序列化响应: response.SerializeToString()
   e) 返回二进制数据

优点：
- 强类型定义，减少错误
- 自动验证数据结构
- 支持二进制传输，节省带宽
- 类型提示文件支持 IDE 智能提示
- 易于扩展和维护
"""
