# 日志系统文档

## 概述

本项目的日志系统提供了结构化的日志记录功能，支持：
- **JSON 列表格式**的日志输出，便于解析和分析
- **Request ID 追踪**，方便问题定位和请求链路追踪
- **分级日志**，支持 DEBUG、INFO、WARNING、ERROR 等不同级别
- **异常追踪**，自动记录完整的异常堆栈信息
- **日志轮转**，自动管理日志文件大小

## 目录结构

```
doc/log/
├── README.md              # 日志系统总览（本文件）
├── architecture.md        # 日志架构设计
├── usage.md              # 使用方法指南
├── request_id.md         # Request ID 详细说明
└── format.md             # 日志格式规范
```

## 快速导航

- [📋 日志格式规范](format.md) - 了解日志输出格式
- [🔧 使用方法](usage.md) - 如何在代码中使用日志
- [🔍 Request ID 追踪](request_id.md) - 请求链路追踪详解
- [🏗️ 架构设计](architecture.md) - 日志系统内部实现

## 核心特性

### 1. 结构化日志格式
所有日志都以 JSON 数组格式输出，便于机器解析：
```json
["2026-03-16T00:51:46.123", "INFO", 12345, 140234567890123, "logger_name", "message", {"key": "value"}]
```

### 2. Request ID 自动追踪
每个 HTTP 请求自动生成唯一的 `request_id`，所有相关日志都会包含此 ID：
- 自动在 `before_request` 钩子中生成
- 贯穿整个请求处理链路
- 支持从客户端请求头中获取外部 `request_id`

### 3. 异常日志分离
异常日志自动记录到独立的 `trace.log` 文件，包含完整的堆栈信息

### 4. 日志轮转
使用 `RotatingFileHandler` 自动管理日志文件：
- 主日志：最大 1MB，保留 5 个备份
- 异常日志：最大 1MB，保留 3 个备份

## 日志文件位置

```
projectTemplate/
├── logs/
│   ├── app.log          # 主日志文件（所有日志）
│   └── trace.log        # 异常日志文件（仅异常）
```

可以通过配置文件自定义日志路径：

```python
from utils.logger import configure_logger_paths

# 配置日志路径
configure_logger_paths(
    log_dir="logs",           # 日志目录
    app_log_file="app.log",   # 主日志文件名
    trace_log_file="trace.log" # 异常日志文件名
)
```

## 使用示例

### 基础日志记录

```python
from utils.logger import setup_logger

logger = setup_logger('my_module')

logger.info("This is an info message")
logger.debug("This is a debug message")
logger.warning("This is a warning")
logger.error("This is an error")
```

### 带 Request ID 的日志

```python
from utils.logger import get_request_id, setup_logger

logger = setup_logger('user_service')

def get_user(user_id):
    request_id = get_request_id()
    logger.info(f"Fetching user {user_id}", extra={'request_id': request_id})
    # ... 业务逻辑 ...
    logger.debug(f"User {user_id} retrieved successfully")
```

### 异常日志

```python
import logging

logger = setup_logger('api_handler')

try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    # 异常会自动记录到 trace.log 并包含完整堆栈
```

## 查看日志

### 实时查看日志

```bash
# 查看主日志
tail -f logs/app.log

# 查看异常日志
tail -f logs/trace.log
```

### 按 Request ID 搜索

```bash
# 搜索特定请求的所有日志
grep "request-id-uuid-here" logs/app.log
```

### 解析 JSON 格式日志

```bash
# 使用 jq 工具解析日志
cat logs/app.log | jq '.[5]'  # 查看 message 字段
cat logs/app.log | jq '.[2]'  # 查看 PID
```

## 配置说明

日志系统支持通过 `config.json` 进行配置：

```json
{
  "logging": {
    "level": "INFO",
    "log_dir": "logs",
    "app_log_file": "app.log",
    "trace_log_file": "trace.log",
    "max_bytes": 1048576,
    "backup_count": 5
  }
}
```

## 相关文档

- [Request ID 使用指南](REQUEST_ID_GUIDE.md) - 详细的 Request ID 使用说明（完整版本）
- [Protocol Buffers 集成](../protobuf/README.md) - 使用 protobuf 定义数据结构

## 最佳实践

1. **始终使用 Request ID**：在 Web 请求中，request_id 会自动包含在日志中
2. **合理使用日志级别**：
   - `DEBUG`: 详细的调试信息
   - `INFO`: 一般信息
   - `WARNING`: 警告信息
   - `ERROR`: 错误信息
3. **记录异常时使用 `exc_info=True`**：自动包含堆栈信息
4. **避免在日志中记录敏感信息**：如密码、token 等
5. **定期清理日志文件**：使用日志轮转或外部日志管理工具
