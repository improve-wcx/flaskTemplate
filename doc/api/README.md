# API 设计指南

## API 规范

### 基础 URL

```
开发环境：http://127.0.0.1:5000/api
生产环境：https://your-domain.com/api
```

### 版本控制

```
/api/v1/users
/api/v2/users
```

## RESTful 设计

### 资源命名

| 方法 | URL | 说明 |
|------|-----|------|
| GET | /api/users | 获取用户列表 |
| GET | /api/users/1 | 获取用户 1 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/1 | 更新用户 1 |
| DELETE | /api/users/1 | 删除用户 1 |

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功 (无内容) |
| 400 | 请求错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 未找到 |
| 500 | 服务器错误 |

## 请求格式

### JSON 请求体

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

### 查询参数

```
GET /api/users?page=1&limit=10
GET /api/users?status=active&sort=name
```

## 响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  "message": "操作成功"
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

### 列表响应

```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10
  }
}
```

## 认证

### Token 认证

```bash
curl -H "Authorization: Bearer your-token-here" \
     http://api.example.com/api/users
```

### API Key

```bash
curl -H "X-API-Key: your-api-key" \
     http://api.example.com/api/users
```

## 速率限制

```
# 响应头
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## 分页

```
GET /api/users?page=1&per_page=20

# 响应
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## 过滤和排序

```
# 过滤
GET /api/users?status=active&role=admin

# 排序
GET /api/users?sort=name&order=asc

# 多字段排序
GET /api/users?sort=name,-created_at
```

## 字段选择

```
# 只返回指定字段
GET /api/users/1?fields=id,name,email
```

## 示例：完整 API 实现

```python
# app/routes/users.py
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')
user_service = UserService()

@users_bp.route('/')
def list_users():
    """
    GET /api/v1/users
    获取用户列表 (支持分页、过滤、排序)
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    # 获取数据
    users, total = user_service.get_users(
        page=page, 
        per_page=per_page,
        status=status
    )
    
    return jsonify({
        'success': True,
        'data': [u.to_dict() for u in users],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }
    })

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    POST /api/v1/users
    创建用户
    """
    data = request.get_json()
    
    # 验证
    if not data or 'name' not in data:
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Name is required'
            }
        }), 400
    
    # 创建
    user = user_service.create_user(
        name=data['name'],
        email=data.get('email')
    )
    
    return jsonify({
        'success': True,
        'data': user.to_dict(),
        'message': 'User created successfully'
    }), 201
```

## 最佳实践

1. **使用 HTTPS** - 生产环境必须
2. **版本控制** - URL 中包含版本号
3. **统一响应格式** - success/data/error 结构
4. **适当的状态码** - 准确反映结果
5. **分页大数据** - 避免返回过多数据
6. **输入验证** - 验证所有输入
7. **错误信息** - 提供清晰的错误提示
8. **文档** - 使用 Swagger/OpenAPI 文档

## 动态 API 列表

本项目支持自动收集和分类所有 API 端点。

### 查询所有可用 API

```bash
# 使用 curl
curl http://127.0.0.1:5000/api/apis

# 使用 CLI
python cli.py apis
```

### 响应格式

```json
{
  "total": 10,
  "apis": {
    "系统": [
      {
        "path": "/api/health",
        "method": "GET",
        "category": "系统",
        "description": "",
        "function": "health_check",
        "module": "api"
      },
      {
        "path": "/api/version",
        "method": "GET",
        "category": "系统",
        "description": "",
        "function": "version",
        "module": "api"
      }
    ],
    "Protobuf 演示": [
      {
        "path": "/api/v1/demo/hello",
        "method": "GET",
        "category": "Protobuf 演示",
        "description": "",
        "function": "hello_get",
        "module": "demo_protobuf"
      }
    ]
  },
  "request_id": "uuid-xxx"
}
```

### 自动分类机制

所有 API 端点会根据其所属的 Blueprint 自动分类：

- `main` Blueprint → **系统**
- `api` Blueprint → **系统**
- `demo_protobuf` Blueprint → **Protobuf 演示**
- `admin` Blueprint → **管理**

添加新 Blueprint 时，在 `app/__init__.py` 中指定分类即可。
