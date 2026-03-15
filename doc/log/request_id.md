# Request ID 追踪系统详解

## 概述

Request ID 是本项目日志系统的核心特性之一。每个 HTTP 请求都会生成一个唯一的 UUID 作为 `request_id`，并在整个请求处理链路中传递。这使得追踪和调试问题变得非常容易。

## 核心概念

### 什么是 Request ID？

- **唯一标识符**: 每个请求都有一个唯一的 UUID（如 `550e8400-e29b-41d4-a716-446655440000`）
- **贯穿整个请求生命周期**: 从请求进入系统到响应返回，所有相关日志都包含此 ID
- **线程安全**: 使用 Python 的 `contextvars` 实现，支持多线程和异步环境
- **自动关联**: 所有日志记录自动包含当前请求的 `request_id`

### 为什么需要 Request ID？

1. **问题定位**: 当用户报告问题时，可以通过 `request_id` 快速找到该请求的所有日志
2. **请求追踪**: 在微服务架构中，可以在不同服务间传递 `request_id` 实现全链路追踪
3. **调试便利**: 开发时可以清晰地看到每个请求的处理过程
4. **日志关联**: 将分散的日志记录关联到同一个请求

## 工作原理

### 1. Request ID 的生成

```python
# 在 app/__init__.py 的 before_request 钩子中
def before_request_handler():
    # 尝试从请求头获取 request_id
    request_id = request.headers.get('X-Request-ID')
    
    if not request_id:
        # 如果没有，生成一个新的 UUID
        request_id = str(uuid.uuid4())
    
    # 设置到上下文
    set_request_id(request_id)
    
    # 存储到 Flask g 对象
    g.request_id = request_id
```

### 2. Request ID 的传递

使用 Python 的 `contextvars` 模块实现：

```python
from contextvars import ContextVar

# 创建上下文变量
_request_id_ctx = ContextVar('request_id', default=None)

def get_request_id():
    """获取当前请求的 request_id"""
    return _request_id_ctx.get()

def set_request_id(request_id):
    """设置当前请求的 request_id"""
    return _request_id_ctx.set(request_id)
```

### 3. Request ID 在日志中的自动包含

```python
class JSONListFormatter(logging.Formatter):
    def format(self, record):
        # 从记录或上下文中获取 request_id
        request_id = getattr(record, 'request_id', None) or _request_id_ctx.get()
        
        # 添加到 extra 字段
        extra = {
            "pathname": record.pathname,
            "lineno": record.lineno,
        }
        
        if request_id:
            extra["request_id"] = request_id
        
        # 构建日志记录
        payload = [timestamp, level, pid, tid, name, message, extra]
        return json.dumps(payload)
```

## 使用方法

### 在 Flask 路由中使用

Request ID 会自动包含在所有日志中，无需手动添加：

```python
from flask import Blueprint, jsonify
from utils.logger import setup_logger

user_bp = Blueprint('user', __name__)
logger = setup_logger('user_routes')

@user_bp.route('/api/users/<user_id>')
def get_user(user_id):
    # 所有日志都会自动包含 request_id
    logger.info(f"Getting user {user_id}")
    
    # 业务逻辑
    user = get_user_from_db(user_id)
    
    logger.debug(f"User data: {user}")
    return jsonify(user)
```

### 在服务层中使用

```python
from utils.logger import setup_logger, get_request_id

class UserService:
    def __init__(self):
        self.logger = setup_logger('user_service')
    
    def create_user(self, username, email):
        # 获取当前 request_id（可选，用于调试）
        request_id = get_request_id()
        self.logger.info(f"Creating user: {username}", extra={'request_id': request_id})
        
        # 业务逻辑
        user = self._save_to_db(username, email)
        
        self.logger.info(f"User created with ID: {user.id}")
        return user
    
    def _save_to_db(self, username, email):
        # 数据库操作
        self.logger.debug(f"Saving to database: {username}")
        # ...
```

### 手动设置 Request ID

在某些情况下，可能需要手动设置 `request_id`：

```python
from utils.logger import set_request_id, reset_request_id

def custom_function():
    # 保存当前的 request_id
    token = set_request_id("custom-request-id-123")
    
    try:
        # 执行一些操作
        do_something()
    finally:
        # 恢复之前的 request_id
        reset_request_id(token)
```

### 从外部获取 Request ID

如果客户端在请求头中提供了 `request_id`，系统会自动使用：

```python
# 客户端请求
curl -X GET http://localhost:5000/api/users \
  -H "X-Request-ID: client-provided-id-123"

# 服务端日志会自动使用这个 ID
# ["2026-03-16T00:51:46.123", "INFO", ..., {"request_id": "client-provided-id-123"}]
```

## 实际应用场景

### 场景 1: 问题排查

用户报告："API 返回 500 错误"

**传统方式**:
1. 询问用户操作时间
2. 在日志文件中按时间搜索
3. 手动翻阅大量日志找到相关记录

**使用 Request ID**:
1. 用户或监控系统提供 `request_id`
2. 直接搜索：`grep "request-id-uuid" logs/app.log`
3. 立即看到该请求的所有日志

### 场景 2: 性能分析

分析某个请求的处理时间：

```bash
# 搜索特定请求的所有日志
grep "550e8400-e29b-41d4-a716-446655440000" logs/app.log

# 输出示例:
# [00:51:46.123] INFO - POST /api/users
# [00:51:46.125] DEBUG - Fetching user data
# [00:51:46.150] DEBUG - Query executed in 25ms
# [00:51:46.155] INFO - Response sent
```

### 场景 3: 微服务追踪

在微服务架构中传递 `request_id`:

```python
# 服务 A
def call_service_b():
    request_id = get_request_id()
    response = requests.get(
        'http://service-b/api/data',
        headers={'X-Request-ID': request_id}
    )
    return response.json()

# 服务 B 的 before_request 钩子会读取 X-Request-ID 并设置到上下文
```

## 日志示例

### 完整请求链路日志

```json
// 1. 请求进入
["2026-03-16T00:51:46.123", "INFO", 230599, 128383944122688, "projectTemplate", 
 "POST /api/v1/users", 
 {"pathname": ".../app/__init__.py", "lineno": 95, "request_id": "abc-123"}]

// 2. 路由处理
["2026-03-16T00:51:46.125", "INFO", 230599, 128383944122688, "user_routes", 
 "Creating new user", 
 {"pathname": ".../app/routes/users.py", "lineno": 42, "request_id": "abc-123"}]

// 3. 服务层处理
["2026-03-16T00:51:46.130", "DEBUG", 230599, 128383944122688, "user_service", 
 "Validating user data", 
 {"pathname": ".../app/services/user.py", "lineno": 78, "request_id": "abc-123"}]

// 4. 数据库操作
["2026-03-16T00:51:46.145", "DEBUG", 230599, 128383944122688, "database", 
 "INSERT INTO users VALUES (...)", 
 {"pathname": ".../app/models/user.py", "lineno": 123, "request_id": "abc-123"}]

// 5. 响应返回
["2026-03-16T00:51:46.150", "INFO", 230599, 128383944122688, "projectTemplate", 
 "POST /api/v1/users 201 127.0.0.1", 
 {"pathname": ".../app/__init__.py", "lineno": 108, "request_id": "abc-123"}]
```

### 异常请求日志

```json
// 1. 请求进入
["2026-03-16T00:52:00.000", "INFO", 230599, 128383944122688, "projectTemplate", 
 "POST /api/v1/users", 
 {"pathname": ".../app/__init__.py", "lineno": 95, "request_id": "def-456"}]

// 2. 验证失败
["2026-03-16T00:52:00.010", "WARNING", 230599, 128383944122688, "user_service", 
 "Validation failed: email is required", 
 {"pathname": ".../app/services/user.py", "lineno": 55, "request_id": "def-456"}]

// 3. 错误响应
["2026-03-16T00:52:00.015", "ERROR", 230599, 128383944122688, "user_routes", 
 "Failed to create user: Validation error", 
 {"pathname": ".../app/routes/users.py", "lineno": 48, 
  "request_id": "def-456",
  "traceback": "Traceback (most recent call last):\n  ..."}]
```

## 配置和自定义

### 禁用 Request ID

如果不需要 Request ID 功能，可以修改 `JSONListFormatter`:

```python
class SimpleFormatter(logging.Formatter):
    def format(self, record):
        # 不包含 request_id
        payload = [timestamp, level, pid, tid, name, message, {}]
        return json.dumps(payload)
```

### 添加自定义字段

```python
class EnhancedFormatter(JSONListFormatter):
    def format(self, record):
        timestamp, level, pid, tid, name, message, extra = super().format(record)
        
        # 添加自定义字段
        extra['environment'] = os.getenv('ENV', 'development')
        extra['version'] = '1.0.0'
        
        payload = [timestamp, level, pid, tid, name, message, extra]
        return json.dumps(payload)
```

## 最佳实践

1. **始终启用 Request ID**: 在生产环境中务必启用此功能
2. **在请求头中传递**: 客户端可以在 `X-Request-ID` 头中提供 ID
3. **日志聚合系统**: 将 `request_id` 作为索引字段，便于搜索
4. **监控告警**: 告警时包含 `request_id`，便于快速定位
5. **不要记录敏感信息**: `request_id` 本身不应包含敏感数据

## 相关文档

- [日志系统总览](README.md)
- [日志格式规范](format.md)
- [使用方法指南](usage.md)
