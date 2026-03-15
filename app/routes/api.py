"""
API routes - for future REST API endpoints
"""
from flask import Blueprint, jsonify, current_app
from utils.logger import get_request_id

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 服务支持的接口列表
AVAILABLE_APIS = [
    {
        "path": "/api/health",
        "method": "GET",
        "description": "健康检查",
        "category": "系统"
    },
    {
        "path": "/api/version",
        "method": "GET",
        "description": "版本信息",
        "category": "系统"
    },
    {
        "path": "/api/v1/demo/hello",
        "method": "GET",
        "description": "简单问候",
        "category": "Protobuf 演示"
    },
    {
        "path": "/api/v1/demo/hello",
        "method": "POST",
        "description": "带参数的问候",
        "category": "Protobuf 演示"
    },
    {
        "path": "/api/v1/demo/user/<user_id>",
        "method": "GET",
        "description": "获取用户信息",
        "category": "Protobuf 演示"
    },
    {
        "path": "/api/v1/demo/users",
        "method": "POST",
        "description": "获取用户列表",
        "category": "Protobuf 演示"
    },
    {
        "path": "/api/v1/demo/echo",
        "method": "POST",
        "description": "Echo 接口",
        "category": "Protobuf 演示"
    },
    {
        "path": "/apis",
        "method": "GET",
        "description": "查询所有可用接口",
        "category": "系统"
    }
]

@api_bp.route('/health')
def health_check():
    """Health check endpoint."""
    request_id = get_request_id()
    current_app.logger.info("Health check", extra={'request_id': request_id})
    return jsonify({'status': 'healthy', 'request_id': request_id})

@api_bp.route('/version')
def version():
    """API version endpoint."""
    request_id = get_request_id()
    return jsonify({'version': '1.0.0', 'request_id': request_id})

@api_bp.route('/apis')
def list_apis():
    """
    查询当前服务支持的所有 Web 接口
    
    返回:
        JSON 格式，包含所有可用接口的详细信息
    """
    request_id = get_request_id()
    
    # 按分类分组
    categorized_apis = {}
    for api in AVAILABLE_APIS:
        category = api['category']
        if category not in categorized_apis:
            categorized_apis[category] = []
        categorized_apis[category].append({
            'path': api['path'],
            'method': api['method'],
            'description': api['description']
        })
    
    return jsonify({
        'total': len(AVAILABLE_APIS),
        'apis': categorized_apis,
        'request_id': request_id
    }), 200
