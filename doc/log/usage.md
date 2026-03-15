# 日志系统使用方法指南

## 快速开始

### 1. 导入和创建 Logger

```python
from utils.logger import setup_logger

# 创建 logger（通常使用模块名）
logger = setup_logger(__name__)
# 或者
logger = setup_logger('my_module')
```

### 2. 记录日志

```python
# 不同级别的日志
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

### 3. 查看日志

```bash
# 实时查看
tail -f logs/app.log

# 查看异常日志
tail -f logs/trace.log
```

## 详细使用

### 基础日志记录

#### 简单消息

```python
logger.info("用户登录成功")
logger.error("数据库连接失败")
```

#### 带变量的消息

```python
user_id = 12345
username = "alice"

logger.info(f"用户 {username} (ID: {user_id}) 登录")
logger.debug(f"处理订单 {order_id}, 金额：${amount}")
```

#### 格式化消息

```python
logger.info("用户 %s 登录，IP: %s", username, ip_address)
logger.warning("API 调用频率限制：%d 次/分钟", request_count)
```

### 异常日志

#### 记录异常堆栈

```python
try:
    result = risky_operation()
except Exception as e:
    # exc_info=True 会自动包含异常堆栈
    logger.error("操作失败：%s", str(e), exc_info=True)
```

#### 捕获特定异常

```python
try:
    user = get_user(user_id)
except UserNotFoundError as e:
    logger.warning("用户不存在：%s", user_id, exc_info=True)
except DatabaseError as e:
    logger.error("数据库错误：%s", str(e), exc_info=True)
```

### 在 Flask 应用中使用

#### 路由中的日志

```python
from flask import Blueprint, request, jsonify
from utils.logger import setup_logger, get_request_id

user_bp = Blueprint('user', __name__)
logger = setup_logger('user_routes')

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # request_id 会自动包含在所有日志中
    logger.info(f"获取用户信息，user_id: {user_id}")
    
    try:
        user = UserService().get_user(user_id)
        logger.debug(f"用户数据：{user}")
        return jsonify(user)
    
    except UserNotFoundError:
        logger.warning(f"用户不存在：{user_id}")
        return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        logger.error(f"获取用户失败：%s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
```

#### 中间件日志

```python
from flask import request
from utils.logger import setup_logger

logger = setup_logger('middleware')

@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path}")
    logger.debug(f"请求头：{dict(request.headers)}")

@app.after_request
def log_response(response):
    logger.info(f"{request.method} {request.path} {response.status_code}")
    return response
```

### 在服务层中使用

```python
from utils.logger import setup_logger

class UserService:
    def __init__(self):
        self.logger = setup_logger('user_service')
    
    def create_user(self, username, email):
        self.logger.info(f"创建用户：{username}")
        
        try:
            # 验证
            self._validate_user(username, email)
            self.logger.debug("用户验证通过")
            
            # 保存到数据库
            user = self._save_to_db(username, email)
            self.logger.info(f"用户创建成功，ID: {user.id}")
            
            return user
        
        except ValidationError as e:
            self.logger.warning(f"用户验证失败：%s", str(e))
            raise
        
        except DatabaseError as e:
            self.logger.error(f"数据库错误：%s", str(e), exc_info=True)
            raise
```

### 在工具函数中使用

```python
from utils.logger import setup_logger

logger = setup_logger('utils')

def parse_json_data(data):
    logger.debug(f"解析 JSON 数据：{data[:100]}...")
    
    try:
        import json
        return json.loads(data)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败：%s", str(e), exc_info=True)
        raise
```

## 配置日志

### 通过代码配置

```python
from utils.logger import setup_logger, configure_logger_paths

# 配置日志路径
configure_logger_paths(
    log_dir="logs",
    app_log_file="app.log",
    trace_log_file="trace.log"
)

# 创建 logger（使用配置的级别）
logger = setup_logger('my_app', level=10)  # 10 = DEBUG
```

### 通过配置文件

在 `config.json` 中配置：

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

加载配置：

```python
import json
from utils.logger import setup_logger, configure_logger_paths

with open('config.json', 'r') as f:
    config = json.load(f)

log_config = config['logging']
configure_logger_paths(
    log_dir=log_config['log_dir'],
    app_log_file=log_config['app_log_file'],
    trace_log_file=log_config['trace_log_file']
)

logger = setup_logger('my_app', level=log_config['level'])
```

### 动态调整日志级别

```python
# 在运行时调整级别
logger.setLevel(logging.DEBUG)  # 开启调试日志
logger.setLevel(logging.INFO)   # 只记录 INFO 及以上

# 临时开启调试模式
import logging
original_level = logger.level
logger.setLevel(logging.DEBUG)
# ... 执行调试操作 ...
logger.setLevel(original_level)
```

## 日志过滤

### 按级别过滤

```python
# 只记录 WARNING 及以上
logger.setLevel(logging.WARNING)

# 只记录 ERROR 及以上
logger.setLevel(logging.ERROR)
```

### 自定义过滤器

```python
class MyFilter(logging.Filter):
    def filter(self, record):
        # 只记录包含特定关键词的日志
        return 'important' in record.getMessage()

logger = setup_logger('my_app')
logger.addFilter(MyFilter())
```

### 分离异常日志

异常日志会自动分离到 `trace.log`：

```python
# 所有日志写入 app.log
logger.info("正常日志")
logger.error("错误日志")

# 只有带 exc_info 的异常日志会写入 trace.log
try:
    risky_operation()
except Exception:
    logger.error("异常日志", exc_info=True)  # 会写入 trace.log
```

## 日志输出示例

### 控制台输出

```bash
["2026-03-16T00:51:46.123", "INFO", 230599, 128383944122688, "user_routes", "用户登录成功", {"pathname": ".../app/routes/users.py", "lineno": 42, "request_id": "abc-123"}]
```

### 文件输出

```bash
# logs/app.log
["2026-03-16T00:51:46.123", "INFO", 230599, 128383944122688, "user_routes", "用户登录成功", {"pathname": ".../app/routes/users.py", "lineno": 42, "request_id": "abc-123"}]
["2026-03-16T00:51:47.456", "DEBUG", 230599, 128383944122688, "user_service", "查询用户数据", {"pathname": ".../app/services/user.py", "lineno": 78, "request_id": "abc-123"}]

# logs/trace.log (仅异常)
["2026-03-16T00:52:00.789", "ERROR", 230599, 128383944122688, "api_handler", "处理请求失败", {"pathname": ".../app/routes/api.py", "lineno": 128, "request_id": "def-456", "traceback": "Traceback (most recent call last):\n  ..."}]
```

## 调试技巧

### 1. 实时查看日志

```bash
# 查看所有日志
tail -f logs/app.log

# 只查看 ERROR 级别
tail -f logs/app.log | grep '"ERROR"'

# 只查看特定 request_id
tail -f logs/app.log | grep "abc-123"
```

### 2. 搜索历史日志

```bash
# 搜索特定用户
grep "user_12345" logs/app.log

# 搜索特定时间段
grep "2026-03-16T00:5[0-9]:" logs/app.log

# 统计错误数量
grep '"ERROR"' logs/app.log | wc -l
```

### 3. 解析 JSON 日志

```bash
# 使用 jq 工具
cat logs/app.log | jq '.[5]'  # 查看消息
cat logs/app.log | jq '.[6].request_id'  # 查看 request_id
```

### 4. Python 脚本分析

```python
import json
from collections import Counter

# 统计各级别日志数量
level_counts = Counter()

with open('logs/app.log', 'r') as f:
    for line in f:
        log_entry = json.loads(line.strip())
        level = log_entry[1]
        level_counts[level] += 1

print("日志级别统计:")
for level, count in level_counts.most_common():
    print(f"  {level}: {count}")
```

## 最佳实践

### 1. 选择合适的日志级别

```python
# ✅ 好的做法
logger.info("用户登录成功")
logger.debug("查询 SQL: SELECT * FROM users WHERE id = %s", user_id)
logger.warning("缓存未命中，从数据库查询")
logger.error("数据库连接失败：%s", str(e), exc_info=True)

# ❌ 不好的做法
logger.debug("用户登录成功")  # 重要信息应该用 INFO
logger.info("SELECT * FROM users")  # SQL 应该用 DEBUG
```

### 2. 避免敏感信息

```python
# ✅ 好的做法
logger.info("用户 %s 登录", username)
logger.info("订单创建成功，ID: %s", order_id)

# ❌ 不好的做法
logger.info("用户登录，密码：%s", password)  # 不要记录密码
logger.info("API Token: %s", token)  # 不要记录 token
```

### 3. 记录足够的上下文

```python
# ✅ 好的做法
logger.info("处理订单 %s，用户 %s，金额 $%.2f", order_id, user_id, amount)

# ❌ 不好的做法
logger.info("处理订单")  # 缺少关键信息
```

### 4. 使用 exc_info 记录异常

```python
# ✅ 好的做法
try:
    result = risky_operation()
except Exception as e:
    logger.error("操作失败：%s", str(e), exc_info=True)

# ❌ 不好的做法
try:
    result = risky_operation()
except Exception as e:
    logger.error("操作失败：%s - %s", str(e), traceback.format_exc())  # 手动格式化
```

### 5. 合理命名 logger

```python
# ✅ 好的做法
logger = setup_logger(__name__)  # 使用模块名
logger = setup_logger('user_service')  # 清晰的组件名

# ❌ 不好的做法
logger = setup_logger('logger')  # 太通用
logger = setup_logger('app')  # 不够具体
```

## 常见问题

### Q: 日志没有输出？

A: 检查日志级别设置：

```python
logger = setup_logger('my_app', level=logging.DEBUG)
```

### Q: 如何禁用文件日志？

A: 可以只保留控制台日志：

```python
logger = setup_logger('my_app')
# 移除文件处理器
for handler in logger.handlers[:]:
    if isinstance(handler, RotatingFileHandler):
        logger.removeHandler(handler)
```

### Q: 如何在测试中禁用日志？

A: 设置日志级别为 CRITICAL：

```python
import logging
logger = setup_logger('my_app', level=logging.CRITICAL)
```

## 相关文档

- [日志系统总览](README.md)
- [日志格式规范](format.md)
- [Request ID 追踪](request_id.md)
- [架构设计](architecture.md)
