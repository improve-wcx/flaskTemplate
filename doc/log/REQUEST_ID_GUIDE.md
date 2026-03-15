# Request ID 追踪日志使用指南

## 概述

为了便于问题定位和调试，系统在 API 请求处理过程中添加了 `request_id` 字段。每个请求都会生成一个唯一的 UUID 作为 `request_id`，并在整个请求处理链路中传递。

## 主要特性

### 1. 自动生成的 Request ID

- 每个 HTTP 请求都会自动生成一个唯一的 UUID 作为 `request_id`
- `request_id` 会在整个请求处理链路中传递（包括路由、服务层、数据库操作等）
- 所有日志记录都会自动包含当前的 `request_id`

### 2. 日志输出格式

日志采用 JSON 数组格式，包含以下字段：
```
[timestamp, level, pid, tid, logger_name, message, extra]
```

其中 `extra` 字段包含：
- `pathname`: 日志输出的文件路径
- `lineno`: 日志输出的行号
- `request_id`: 当前请求的唯一标识符（如果存在）
- `traceback`: 异常堆栈信息（如果有异常）

### 3. 服务端 Request ID

每个请求会在服务端自动生成一个唯一的 `request_id`，用于日志追踪和问题定位。`request_id` 不会通过响应头返回给客户端，仅在服务端内部使用。

## 使用方法

### 在路由中使用

```python
from flask import current_app
from utils.logger import get_request_id

@main_bp.route('/')
def hello():
    request_id = get_request_id()
    current_app.logger.info("Handling request", extra={'request_id': request_id})
    return "Hello, World!"
```

### 在服务层中使用

```python
from app.services.base import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__('user_service')
    
    def get_user(self, user_id: int):
        self.info(f"Fetching user {user_id}")  # 自动包含 request_id
        # ... user fetching logic ...
        self.debug(f"User {user_id} fetched successfully")
```

### 手动设置 Request ID

如果需要手动设置 `request_id`（例如从请求头中获取）：

```python
from utils.logger import set_request_id, reset_request_id

def before_request():
    # 尝试从请求头获取 request_id
    request_id = request.headers.get('X-Request-ID')
    if not request_id:
        # 如果没有，生成一个新的
        request_id = set_request_id()
    else:
        # 使用客户端提供的 request_id
        token = set_request_id(request_id)
```

## 日志示例

### 正常请求日志

```json
["2026-03-16T00:51:46.123", "INFO", 12345, 140234567890123, "projectTemplate", "GET /api/health", {"pathname": "/home/wcx/code/projectTemplate/app/__init__.py", "lineno": 95, "request_id": "550e8400-e29b-41d4-a716-446655440000"}]
```

### 带异常的日志

```json
["2026-03-16T00:51:47.456", "ERROR", 12345, 140234567890123, "user_service", "Failed to fetch user", {"pathname": "/home/wcx/code/projectTemplate/app/services/user.py", "lineno": 42, "request_id": "550e8400-e29b-41d4-a716-446655440000", "traceback": "Traceback (most recent call last):\n  ..."}]
```

## 调试技巧

### 1. 追踪完整请求链路

使用 `request_id` 可以在日志文件中搜索整个请求的所有日志：

```bash
# 搜索特定 request_id 的所有日志
grep "550e8400-e29b-41d4-a716-446655440000" logs/app.log

# 使用 jq 格式化查看（如果安装了 jq）
grep "550e8400-e29b-41d4-a716-446655440000" logs/app.log | jq .
```

### 2. 查看错误日志

```bash
# 查看所有错误日志
grep "ERROR" logs/app.log

# 查看特定时间段的错误
tail -n 100 logs/app.log | grep "ERROR"
```

### 3. 实时监控日志

```bash
# 实时监控日志
tail -f logs/app.log

# 实时监控并过滤特定 request_id
tail -f logs/app.log | grep "550e8400-e29b-41d4-a716-446655440000"
```

## API 响应示例

### 健康检查响应

```json
{
  "status": "healthy",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

注意：`request_id` 仅在 API 响应中返回，不在响应头中。

## 最佳实践

1. **始终使用 `get_request_id()` 获取当前请求 ID**，不要手动生成
2. **在关键业务逻辑处记录日志**，便于追踪问题
3. **使用 `BaseService` 类** 作为服务的基础类，自动处理 `request_id`
4. **在 API 响应中返回 `request_id`**，方便客户端反馈问题
5. **在日志中记录足够的上下文信息**，但不要过于冗长

## 常见问题

### Q: 如何在异步任务中使用 request_id？

A: 在启动异步任务时，手动传递 `request_id`：

```python
from utils.logger import get_request_id, set_request_id

def start_async_task():
    request_id = get_request_id()
    # 在异步任务中
    def async_job():
        token = set_request_id(request_id)
        try:
            # 业务逻辑
            pass
        finally:
            reset_request_id(token)
```

### Q: 如何禁用 request_id？

A: 目前不支持禁用，因为 `request_id` 对于问题定位非常重要。

### Q: Request ID 的格式是什么？

A: 使用 UUID v4 格式，例如：`550e8400-e29b-41d4-a716-446655440000`
