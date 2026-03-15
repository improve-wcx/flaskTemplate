# 项目架构

## 整体架构

```
┌─────────────────────────────────────────┐
│          客户端 (Browser/API)            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         WSGI Server (Gunicorn)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Flask Application             │
│  ┌──────────────────────────────────┐   │
│  │         app/__init__.py          │   │
│  │       (Application Factory)      │   │
│  └──────────────────────────────────┘   │
│         │              │                 │
│  ┌──────▼────┐  ┌─────▼─────┐          │
│  │  Routes   │  │  Config   │          │
│  │ (Blueprint)│  │  (JSON)   │          │
│  └───────────┘  └───────────┘          │
│         │                              │
│  ┌──────▼──────┐  ┌──────────┐        │
│  │   Models    │  │ Services │        │
│  │ (Data)      │  │ (Logic)  │        │
│  └─────────────┘  └──────────┘        │
└─────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Logging System                 │
│  ┌────────────┐  ┌────────────┐        │
│  │  app.log   │  │ trace.log  │        │
│  │ (General)  │  │ (Errors)   │        │
│  └────────────┘  └────────────┘        │
└─────────────────────────────────────────┘
```

## 核心组件

### 1. 应用工厂 (app/__init__.py)

使用工厂模式创建 Flask 应用：

```python
def create_app(config_name=None):
    app = Flask(__name__)
    config = get_config(config_name)
    # 应用配置
    # 注册蓝图
    # 初始化日志
    return app
```

**优点**：
- 支持多环境配置
- 便于测试
- 灵活的应用创建

### 2. 路由层 (app/routes/)

使用 Flask Blueprint 模块化路由：

```
routes/
├── main.py      # 主路由 (/)
├── api.py       # API 路由 (/api/)
└── admin.py     # 管理路由 (/admin/)
```

**每个蓝图负责**：
- 定义路由规则
- 处理请求
- 返回响应

### 3. 配置系统 (config/)

JSON 配置文件统一管理：

```python
from config import get_config
config = get_config('development')
host = config['app']['host']
```

**配置层次**：
1. `config.json` - 基础配置
2. 环境变量 - 敏感信息
3. 运行时参数 - 临时覆盖

### 4. 数据模型层 (app/models/)

定义数据结构：

```python
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}
```

### 5. 服务层 (app/services/)

业务逻辑封装：

```python
class UserService:
    def create_user(self, name, email):
        # 业务逻辑
        user = User(name, email)
        self.save(user)
        return user
```

### 6. 日志系统 (utils/logger.py)

结构化日志记录：

- JSON 格式输出
- 自动轮转
- 异常追踪

## 请求流程

```
1. 请求到达
   ↓
2. WSGI 服务器接收
   ↓
3. Flask 应用处理
   ↓
4. 路由匹配 (Blueprint)
   ↓
5. 调用视图函数
   ↓
6. (可选) 服务层业务逻辑
   ↓
7. (可选) 模型层数据操作
   ↓
8. 返回响应
   ↓
9. 日志记录
```

## 扩展指南

### 添加新功能

1. **添加路由** → `app/routes/new_feature.py`
2. **注册蓝图** → `app/__init__.py`
3. **添加模型** → `app/models/new_feature.py`
4. **添加服务** → `app/services/new_feature.py`
5. **编写测试** → `tests/test_routes/test_new_feature.py`

### 配置新环境

编辑 `config/config.json`:

```json
{
  "staging": {
    "app": { "host": "0.0.0.0", "port": 5000 },
    "logging": { "level": "WARNING" }
  }
}
```

## 最佳实践

1. **单一职责** - 每个模块专注一个功能
2. **依赖注入** - 通过参数传递依赖
3. **配置分离** - 配置与代码分离
4. **日志记录** - 关键操作都要记录
5. **单元测试** - 核心功能必须有测试

## 技术栈

- **Web 框架**: Flask 2.3.3
- **配置管理**: JSON 配置文件
- **日志**: RotatingFileHandler
- **测试**: pytest 9.0
- **部署**: Gunicorn/uWSGI
