# 日志格式规范

## 概述

本项目的日志采用**JSON 数组（列表）**格式，每个日志记录都是一个包含 7 个元素的数组。这种格式便于机器解析、日志聚合和分析。

## 日志记录结构

每个日志记录是一个 JSON 数组，包含以下字段：

```json
[
  "2026-03-16T00:51:46.123",  // [0] timestamp: 时间戳
  "INFO",                      // [1] level: 日志级别
  12345,                       // [2] pid: 进程 ID
  140234567890123,             // [3] tid: 线程 ID
  "logger_name",               // [4] logger_name: 日志记录器名称
  "message",                   // [5] message: 日志消息
  {"key": "value"}             // [6] extra: 额外信息（字典）
]
```

### 字段详细说明

#### 0. timestamp (时间戳)
- **类型**: 字符串
- **格式**: `YYYY-MM-DDTHH:MM:SS.mmm`
- **示例**: `"2026-03-16T00:51:46.123"`
- **说明**: 精确到毫秒的 ISO 8601 格式时间戳

#### 1. level (日志级别)
- **类型**: 字符串
- **可选值**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **示例**: `"INFO"`, `"ERROR"`
- **说明**: 表示日志的重要程度

#### 2. pid (进程 ID)
- **类型**: 整数
- **示例**: `12345`
- **说明**: 生成日志的进程 ID，便于在多进程环境中追踪

#### 3. tid (线程 ID)
- **类型**: 整数
- **示例**: `140234567890123`
- **说明**: 生成日志的线程 ID，便于在多线程环境中追踪

#### 4. logger_name (日志记录器名称)
- **类型**: 字符串
- **示例**: `"app.routes.api"`, `"user_service"`, `"projectTemplate"`
- **说明**: 日志记录器的名称，通常是模块名或组件名

#### 5. message (日志消息)
- **类型**: 字符串
- **示例**: `"User 123 logged in"`, `"Processing request /api/users"`
- **说明**: 日志的主要内容，描述发生的事件

#### 6. extra (额外信息)
- **类型**: 字典（JSON 对象）
- **结构**:
  ```json
  {
    "pathname": "/path/to/file.py",
    "lineno": 42,
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "traceback": "Traceback (most recent call last):\n..."
  }
  ```
- **字段说明**:
  - `pathname`: 日志输出的文件路径（可选）
  - `lineno`: 日志输出的行号（可选）
  - `request_id`: 当前请求的唯一标识符（可选，Web 请求中自动包含）
  - `traceback`: 异常堆栈信息（仅在异常日志中存在）

## 日志示例

### 1. 正常请求日志

```json
[
  "2026-03-16T00:51:46.123",
  "INFO",
  230599,
  128383944122688,
  "projectTemplate",
  "POST /api/v1/hello",
  {
    "pathname": "/home/wcx/code/projectTemplate/app/__init__.py",
    "lineno": 95,
    "request_id": "a27c7dd3-eaea-457e-8eac-3039b44df135"
  }
]
```

### 2. 业务日志

```json
[
  "2026-03-16T00:51:47.456",
  "DEBUG",
  230599,
  128383944122688,
  "user_service",
  "Fetching user with ID 12345",
  {
    "pathname": "/home/wcx/code/projectTemplate/app/services/user.py",
    "lineno": 42,
    "request_id": "a27c7dd3-eaea-457e-8eac-3039b44df135"
  }
]
```

### 3. 异常日志（包含 traceback）

```json
[
  "2026-03-16T00:51:48.789",
  "ERROR",
  230599,
  128383944122688,
  "api_handler",
  "Failed to process request",
  {
    "pathname": "/home/wcx/code/projectTemplate/app/routes/api.py",
    "lineno": 128,
    "request_id": "a27c7dd3-eaea-457e-8eac-3039b44df135",
    "traceback": "Traceback (most recent call last):\n  File \"/home/wcx/code/projectTemplate/app/routes/api.py\", line 125, in process\n    result = do_something()\n  File \"/home/wcx/code/projectTemplate/app/services/something.py\", line 42, in do_something\n    raise ValueError(\"Invalid input\")\nValueError: Invalid input\n"
  }
]
```

### 4. 警告日志

```json
[
  "2026-03-16T00:51:49.012",
  "WARNING",
  230599,
  128383944122688,
  "cache_service",
  "Cache miss for key: user_12345",
  {
    "pathname": "/home/wcx/code/projectTemplate/app/services/cache.py",
    "lineno": 78,
    "request_id": "a27c7dd3-eaea-457e-8eac-3039b44df135"
  }
]
```

## 日志级别说明

| 级别 | 数值 | 说明 | 使用场景 |
|------|------|------|----------|
| DEBUG | 10 | 调试信息 | 详细的调试信息，开发阶段使用 |
| INFO | 20 | 一般信息 | 正常的业务流程，如请求处理、状态变更 |
| WARNING | 30 | 警告信息 | 非错误但需要注意的情况，如缓存未命中、使用废弃 API |
| ERROR | 40 | 错误信息 | 错误但程序仍能继续运行，如数据库连接失败 |
| CRITICAL | 50 | 严重错误 | 严重错误，程序可能无法继续运行 |

## 日志文件

### 1. 主日志文件 (`app.log`)

- **位置**: `logs/app.log`
- **内容**: 所有级别的日志（DEBUG 及以上）
- **格式**: JSON 数组
- **轮转策略**: 最大 1MB，保留 5 个备份

### 2. 异常日志文件 (`trace.log`)

- **位置**: `logs/trace.log`
- **内容**: 仅包含异常日志（ERROR 及以上，且包含 `exc_info`）
- **格式**: JSON 数组（包含完整的 traceback）
- **轮转策略**: 最大 1MB，保留 3 个备份

## 解析日志

### 使用 Python 解析

```python
import json

with open('logs/app.log', 'r') as f:
    for line in f:
        log_entry = json.loads(line.strip())
        timestamp, level, pid, tid, logger_name, message, extra = log_entry
        
        print(f"[{timestamp}] {level} - {message}")
        if 'request_id' in extra:
            print(f"  Request ID: {extra['request_id']}")
        if 'traceback' in extra:
            print(f"  Traceback: {extra['traceback']}")
```

### 使用 jq 解析（命令行）

```bash
# 查看所有日志的消息字段
cat logs/app.log | jq '.[5]'

# 查看特定级别的日志
cat logs/app.log | jq 'select(.[1] == "ERROR")'

# 统计各级别的日志数量
cat logs/app.log | jq -r '.[1]' | sort | uniq -c

# 搜索包含特定 request_id 的日志
cat logs/app.log | jq 'select(.[6].request_id == "550e8400-e29b-41d4-a716-446655440000")'
```

### 使用 grep 搜索

```bash
# 搜索包含 request_id 的日志
grep "request_id" logs/app.log

# 搜索 ERROR 级别的日志
grep '"ERROR"' logs/app.log

# 搜索特定路径的日志
grep "user_service" logs/app.log
```

## 自定义日志格式

如果需要自定义日志格式，可以继承 `JSONListFormatter`：

```python
from utils.logger import JSONListFormatter
import json

class CustomFormatter(JSONListFormatter):
    def format(self, record):
        # 在原有格式基础上添加自定义字段
        timestamp, level, pid, tid, name, message, extra = super().format(record)
        
        # 添加自定义字段
        extra['custom_field'] = 'custom_value'
        
        # 重新构建日志记录
        payload = [timestamp, level, pid, tid, name, message, extra]
        return json.dumps(payload, ensure_ascii=False)
```

## 最佳实践

1. **保持消息简洁**: message 字段应该简洁明了，避免过长
2. **使用结构化数据**: 复杂信息放在 `extra` 字典中
3. **避免敏感信息**: 不要在日志中记录密码、token 等敏感数据
4. **合理使用日志级别**: 根据重要性选择合适的级别
5. **包含上下文信息**: 在 `extra` 中添加有助于问题定位的信息

## 相关文档

- [日志系统总览](README.md)
- [Request ID 追踪](request_id.md)
- [使用方法指南](usage.md)
