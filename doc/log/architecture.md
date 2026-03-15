# 日志系统架构设计

## 概述

本文档详细描述了日志系统的内部实现架构，包括组件设计、数据流、配置机制等。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      应用层 (Application)                     │
├─────────────────────────────────────────────────────────────┤
│  Flask Routes  │  Services  │  Models  │  Utils             │
│  (logger.info) │ (logger)   │ (logger) │ (logger)           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    日志核心层 (Logger Core)                   │
├─────────────────────────────────────────────────────────────┤
│  setup_logger()  │  JSONListFormatter  │  ContextVars       │
│  - 创建 logger   │  - 格式化输出       │  - request_id 管理  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   日志处理层 (Handler Layer)                  │
├─────────────────────────────────────────────────────────────┤
│  RotatingFileHandler  │  StreamHandler  │  ExceptionFilter  │
│  - app.log (主日志)   │  - 控制台输出   │  - 异常过滤       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    日志存储层 (Storage)                       │
├─────────────────────────────────────────────────────────────┤
│  logs/app.log    │  logs/trace.log                          │
│  - 所有日志      │  - 仅异常日志                             │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Logger 创建器 (`setup_logger`)

**职责**: 创建和配置 logger 实例

**实现**:
```python
def setup_logger(name: str = None, level: int = logging.DEBUG) -> logging.Logger:
    """
    创建配置好的 logger
    
    配置:
    - 格式：JSON 列表格式
    - 处理器: 文件 + 控制台
    - 级别: DEBUG 及以上
    """
    logger = logging.getLogger(name)
    
    # 添加文件处理器 (RotatingFileHandler)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(JSONListFormatter())
    logger.addHandler(file_handler)
    
    # 添加控制台处理器
    console_handler = StreamHandler()
    console_handler.setFormatter(JSONListFormatter())
    logger.addHandler(console_handler)
    
    # 添加异常追踪处理器
    trace_handler = RotatingFileHandler(
        LOG_TRACE_FILE,
        maxBytes=1024*1024,
        backupCount=3
    )
    trace_handler.addFilter(ExceptionOnlyFilter())
    trace_handler.setFormatter(JSONListFormatter())
    logger.addHandler(trace_handler)
    
    return logger
```

### 2. 日志格式化器 (`JSONListFormatter`)

**职责**: 将日志记录格式化为 JSON 数组

**数据结构**:
```python
[
    timestamp,    # 时间戳 (string)
    level,        # 日志级别 (string)
    pid,          # 进程 ID (int)
    tid,          # 线程 ID (int)
    name,         # logger 名称 (string)
    message,      # 消息 (string)
    extra         # 额外信息 (dict)
]
```

**实现**:
```python
class JSONListFormatter(logging.Formatter):
    def format(self, record):
        # 提取各个字段
        timestamp = self.formatTime(record)
        level = record.levelname
        pid = record.process
        tid = record.thread
        name = record.name
        message = record.getMessage()
        
        # 获取 request_id
        request_id = getattr(record, 'request_id', None) or _request_id_ctx.get()
        
        # 构建 extra 字典
        extra = {
            "pathname": record.pathname,
            "lineno": record.lineno,
        }
        if request_id:
            extra["request_id"] = request_id
        if record.exc_info:
            extra["traceback"] = ''.join(traceback.format_exception(*record.exc_info))
        
        # 返回 JSON 数组
        payload = [timestamp, level, pid, tid, name, message, extra]
        return json.dumps(payload)
```

### 3. Request ID 上下文管理

**职责**: 在多线程/异步环境中管理 request_id

**实现**:
```python
from contextvars import ContextVar

# 创建上下文变量
_request_id_ctx = ContextVar('request_id', default=None)

def get_request_id():
    """获取当前上下文中的 request_id"""
    return _request_id_ctx.get()

def set_request_id(request_id):
    """设置当前上下文中的 request_id"""
    return _request_id_ctx.set(request_id)

def reset_request_id(token):
    """重置 request_id 到之前的值"""
    _request_id_ctx.reset(token)
```

**为什么使用 ContextVar?**
- 线程安全：每个线程有独立的值
- 异步安全：每个 async 任务有独立的值
- 自动清理：任务结束后自动释放

### 4. 异常过滤器 (`ExceptionOnlyFilter`)

**职责**: 只允许包含异常信息的日志通过

**实现**:
```python
class ExceptionOnlyFilter(logging.Filter):
    def filter(self, record):
        # 只有包含异常信息的记录才通过
        return bool(record.exc_info)
```

**用途**: 将异常日志分离到独立的 `trace.log` 文件

## 数据流

### 正常日志流程

```
1. 应用层调用 logger.info("message")
                    │
                    ▼
2. Logger 创建 LogRecord 对象
   - 包含: 时间、级别、消息、堆栈等
                    │
                    ▼
3. 通过所有 Handler
   ├─ FileHandler → JSONListFormatter → app.log
   ├─ ConsoleHandler → JSONListFormatter → 控制台
   └─ TraceHandler → (被过滤器拦截，不输出)
```

### 异常日志流程

```
1. 应用层调用 logger.error("error", exc_info=True)
                    │
                    ▼
2. Logger 创建 LogRecord 对象
   - exc_info 包含异常堆栈
                    │
                    ▼
3. 通过所有 Handler
   ├─ FileHandler → JSONListFormatter → app.log
   ├─ ConsoleHandler → JSONListFormatter → 控制台
   └─ TraceHandler → ExceptionFilter → 通过 → trace.log
```

### Request ID 传递流程

```
1. 请求进入 Flask
                    │
                    ▼
2. before_request 钩子
   - 生成/获取 request_id
   - set_request_id(request_id)
                    │
                    ▼
3. 路由处理
   - logger.info("处理请求")
   - JSONListFormatter 自动获取 request_id
                    │
                    ▼
4. 日志输出
   - 包含 request_id 的 JSON 数组
                    │
                    ▼
5. after_request 钩子
   - 可选：清理 request_id
```

## 配置机制

### 1. 路径配置

```python
def configure_logger_paths(log_dir, app_log_file, trace_log_file):
    """
    配置日志文件路径
    
    支持:
    - 相对路径 (相对于项目根目录)
    - 绝对路径
    """
    global LOG_DIR, LOG_FILE, LOG_TRACE_FILE
    
    # 处理相对路径
    if not os.path.isabs(log_dir):
        log_dir = os.path.join(PROJECT_ROOT, log_dir)
    
    LOG_DIR = log_dir
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, app_log_file)
    LOG_TRACE_FILE = os.path.join(LOG_DIR, trace_log_file)
```

### 2. 级别配置

```python
# 通过参数设置
logger = setup_logger('my_app', level=logging.DEBUG)

# 通过配置文件
config = load_config()
level = getattr(logging, config['logging']['level'])
logger = setup_logger('my_app', level=level)
```

### 3. 运行时配置

```python
# 动态调整级别
logger.setLevel(logging.WARNING)

# 动态添加处理器
new_handler = RotatingFileHandler('custom.log')
logger.addHandler(new_handler)

# 动态移除处理器
logger.removeHandler(old_handler)
```

## 线程安全和异步安全

### 多线程环境

```python
import threading
from utils.logger import setup_logger

logger = setup_logger('multi_thread')

def worker(thread_id):
    logger.info(f"Thread {thread_id} started")
    # 每个线程有独立的 request_id 上下文
    logger.info(f"Thread {thread_id} processing")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### 异步环境

```python
import asyncio
from utils.logger import setup_logger

logger = setup_logger('async_app')

async def handle_request(request_id):
    # 设置 request_id
    set_request_id(request_id)
    
    logger.info(f"Handling request {request_id}")
    await asyncio.sleep(0.1)
    logger.info(f"Request {request_id} completed")

async def main():
    # 并发处理多个请求
    await asyncio.gather(
        handle_request("req-1"),
        handle_request("req-2"),
        handle_request("req-3")
    )

asyncio.run(main())
```

## 性能优化

### 1. 异步日志 (可选)

对于高并发场景，可以使用异步日志：

```python
from queue import Queue
from logging.handlers import QueueHandler, QueueListener

# 创建队列
log_queue = Queue()

# 创建 QueueHandler
queue_handler = QueueHandler(log_queue)

# 创建 QueueListener
listener = QueueListener(log_queue, file_handler, console_handler)
listener.start()

# 添加 QueueHandler 到 logger
logger.addHandler(queue_handler)
```

### 2. 日志采样

对于高频日志，可以使用采样：

```python
import logging

# 1% 的采样率
logger.setLevel(logging.DEBUG)
logger.addFilter(logging.Filter('sampled'))

# 或者使用 logging.handlers.RotatingFileHandler 的 maxBytes
```

### 3. 批量写入

```python
# 使用 MemoryHandler 批量写入
from logging.handlers import MemoryHandler

memory_handler = MemoryHandler(
    capacity=100,  # 缓冲区大小
    flushLevel=logging.INFO,  # 达到 INFO 级别时刷新
    target=file_handler
)
logger.addHandler(memory_handler)
```

## 扩展和定制

### 自定义 Formatter

```python
class CustomFormatter(JSONListFormatter):
    def format(self, record):
        # 在原有格式基础上添加自定义字段
        timestamp, level, pid, tid, name, message, extra = super().format(record)
        
        # 添加自定义字段
        extra['environment'] = os.getenv('ENV', 'development')
        extra['version'] = '1.0.0'
        
        payload = [timestamp, level, pid, tid, name, message, extra]
        return json.dumps(payload)
```

### 自定义 Handler

```python
class DatabaseHandler(logging.Handler):
    """将日志写入数据库"""
    
    def emit(self, record):
        log_entry = self.format(record)
        # 写入数据库
        db.insert_log(log_entry)
```

### 自定义 Filter

```python
class RateLimitFilter(logging.Filter):
    """日志速率限制"""
    
    def __init__(self, name='', limit=100):
        super().__init__(name)
        self.limit = limit
        self.count = 0
        self.last_reset = time.time()
    
    def filter(self, record):
        # 每分钟限制 100 条日志
        if time.time() - self.last_reset > 60:
            self.count = 0
            self.last_reset = time.time()
        
        if self.count < self.limit:
            self.count += 1
            return True
        return False
```

## 监控和告警

### 日志监控

```python
import re

def monitor_error_logs(log_file, callback):
    """监控错误日志"""
    error_pattern = re.compile('"ERROR"')
    
    with open(log_file, 'r') as f:
        for line in f:
            if error_pattern.search(line):
                callback(line)

# 使用
def alert_handler(log_entry):
    send_alert(f"错误日志：{log_entry}")

monitor_error_logs('logs/app.log', alert_handler)
```

### 日志分析

```python
import json
from collections import Counter

def analyze_logs(log_file):
    """分析日志文件"""
    level_counts = Counter()
    error_messages = []
    
    with open(log_file, 'r') as f:
        for line in f:
            entry = json.loads(line.strip())
            level_counts[entry[1]] += 1
            
            if entry[1] == 'ERROR':
                error_messages.append(entry[5])
    
    return {
        'level_distribution': dict(level_counts),
        'top_errors': Counter(error_messages).most_common(10)
    }
```

## 相关文档

- [日志系统总览](README.md)
- [使用方法指南](usage.md)
- [日志格式规范](format.md)
- [Request ID 追踪](request_id.md)
