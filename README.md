# Flask Project Template

一个结构化的 Flask 项目模板，支持模块化开发和多环境配置。

## 项目结构

```
projectTemplate/
├── app/                    # 主应用包
│   ├── __init__.py        # 应用工厂
│   ├── routes/            # 路由模块
│   │   ├── main.py        # 主路由
│   │   ├── api.py         # API 路由
│   │   └── admin.py       # 管理后台路由
│   ├── models/            # 数据模型（待扩展）
│   ├── services/          # 业务逻辑层（待扩展）
│   ├── templates/         # HTML 模板
│   └── static/            # 静态文件
├── config/                # 配置文件
│   ├── base.py           # 基础配置
│   ├── development.py    # 开发环境
│   ├── testing.py        # 测试环境
│   └── production.py     # 生产环境
├── utils/                 # 工具函数
│   └── logger.py         # 日志配置
├── tests/                 # 测试目录
│   ├── conftest.py       # pytest 配置
│   └── test_routes/      # 路由测试
├── logs/                  # 日志目录（gitignore 排除）
├── run.py                 # 启动入口
├── wsgi.py                # WSGI 入口
├── requirements.txt       # 依赖
└── .env.example          # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac
# 或 env\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements-dev.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件设置你的配置
```

### 3. 运行应用

#### 开发模式

```bash
# 方式 1: 使用 run.py
python run.py

# 方式 2: 使用 Flask 命令
export FLASK_ENV=development
flask run

# 访问 http://127.0.0.1:5000
```

**开发模式特点**：
- 自动重载代码更改
- 启用调试器（错误页面显示详细信息）
- 日志级别为 DEBUG
- 适合本地开发调试

#### 生产环境

```bash
# 使用 Gunicorn（推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# 或使用 uWSGI
uwsgi --http :5000 --module wsgi:app --master --processes 4
```

**生产环境特点**：
- 多进程/多线程处理请求
- 日志级别为 INFO
- 禁用调试器
- 更安全的会话配置

### 4. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_routes/test_main.py -v

# 运行特定测试函数
pytest tests/test_routes/test_main.py::test_hello_route_returns_hello_world -v

# 生成测试覆盖率报告
pytest tests/ --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html  # macOS
# 或 xdg-open htmlcov/index.html  # Linux
```

---

## 配置管理

### 配置文件结构

```
config/
├── base.py          # 基础配置（所有环境共享）
├── development.py   # 开发环境配置
├── testing.py       # 测试环境配置
└── production.py    # 生产环境配置
```

### 修改配置

1. **添加新配置项**：在 `config/base.py` 的 `BaseConfig` 类中添加

```python
# config/base.py
class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 新增配置项
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 最大上传大小
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf'}
```

2. **环境特定配置**：在对应环境配置类中覆盖

```python
# config/production.py
class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')  # 必须从环境变量获取
    
    # 覆盖基础配置
    LOG_LEVEL = 'WARNING'
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64MB
```

3. **使用环境变量**（推荐）

```bash
# .env 文件
SECRET_KEY=your-secure-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
LOG_LEVEL=INFO
```

4. **切换环境**

```bash
# 开发环境
export FLASK_ENV=development
python run.py

# 生产环境
export FLASK_ENV=production
gunicorn wsgi:app

# 测试环境
export FLASK_ENV=testing
pytest
```

---

## 开发指南

### 添加新的 API 接口

#### 步骤 1: 创建路由

在 `app/routes/` 目录下创建或修改路由文件：

```python
# app/routes/users.py
from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/')
def get_users():
    """获取所有用户列表"""
    # 示例数据
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return jsonify(users)

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    """获取指定用户信息"""
    # 示例：根据 ID 查找用户
    user = {'id': user_id, 'name': f'User {user_id}'}
    return jsonify(user)

@users_bp.route('/', methods=['POST'])
def create_user():
    """创建新用户"""
    data = request.get_json()
    
    # 验证请求数据
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # 创建用户逻辑
    new_user = {
        'id': 3,
        'name': data['name']
    }
    
    return jsonify(new_user), 201
```

#### 步骤 2: 注册蓝图

在 `app/__init__.py` 中注册新路由：

```python
# app/__init__.py
from flask import Flask
from utils.logger import setup_logger

def create_app(config_name=None):
    if config_name is None:
        import os
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config.base import config_map
    config_class = config_map.get(config_name, config_map['default'])
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logger = setup_logger("projectTemplate")
    app.logger = logger
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.users import users_bp  # 导入新路由
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(users_bp)  # 注册新路由
    
    # ... 其他配置
    
    return app
```

#### 步骤 3: 测试新接口

```bash
# 启动应用
python run.py

# 测试接口
curl http://127.0.0.1:5000/api/users/
curl http://127.0.0.1:5000/api/users/1
curl -X POST http://127.0.0.1:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'
```

### 添加 Web 页面（模板）

#### 步骤 1: 创建 HTML 模板

```html
<!-- app/templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

#### 步骤 2: 添加路由

```python
# app/routes/pages.py
from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/home')
def home():
    """渲染首页"""
    return render_template('index.html', 
                         title='首页',
                         message='欢迎',
                         items=['项目 1', '项目 2', '项目 3'])
```

#### 步骤 3: 注册并访问

```python
# app/__init__.py
from app.routes.pages import pages_bp
app.register_blueprint(pages_bp)
```

访问：`http://127.0.0.1:5000/home`

### 添加数据模型

```python
# app/models/user.py
from datetime import datetime

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
```

### 添加业务逻辑层

```python
# app/services/user_service.py
from app.models.user import User

class UserService:
    def __init__(self):
        self.users = []
    
    def get_all_users(self):
        return self.users
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def create_user(self, name, email):
        new_id = len(self.users) + 1
        user = User(new_id, name, email)
        self.users.append(user)
        return user
```

---

## 单元测试指南

### 测试结构

```
tests/
├── conftest.py           # pytest 配置和共享 fixture
└── test_routes/          # 路由测试
    ├── test_main.py      # 主路由测试
    ├── test_api.py       # API 路由测试
    └── test_users.py     # 用户路由测试（新）
```

### 编写新的单元测试

#### 示例：为 users 路由添加测试

```python
# tests/test_routes/test_users.py
import json

def test_get_users(client):
    """测试获取用户列表"""
    resp = client.get('/api/users/')
    
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user_by_id(client):
    """测试获取指定用户"""
    resp = client.get('/api/users/1')
    
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert 'id' in data
    assert data['id'] == 1

def test_create_user(client):
    """测试创建用户"""
    new_user = {'name': 'Test User'}
    
    resp = client.post(
        '/api/users/',
        data=json.dumps(new_user),
        content_type='application/json'
    )
    
    assert resp.status_code == 201
    
    data = resp.get_json()
    assert data['name'] == 'Test User'
    assert 'id' in data

def test_create_user_missing_name(client):
    """测试创建用户时缺少必填字段"""
    invalid_user = {'email': 'test@example.com'}
    
    resp = client.post(
        '/api/users/',
        data=json.dumps(invalid_user),
        content_type='application/json'
    )
    
    assert resp.status_code == 400
    
    data = resp.get_json()
    assert 'error' in data
```

### 使用 Fixture

```python
# tests/test_routes/test_custom.py
import pytest
from app.models.user import User

@pytest.fixture
def sample_user():
    """提供示例用户"""
    return User(1, 'Alice', 'alice@example.com')

def test_user_to_dict(sample_user):
    """测试用户模型"""
    result = sample_user.to_dict()
    
    assert result['name'] == 'Alice'
    assert result['email'] == 'alice@example.com'
    assert 'created_at' in result
```

### 测试数据库操作（示例）

```python
# tests/test_services/test_user_service.py
from app.services.user_service import UserService

def test_create_user():
    """测试用户服务"""
    service = UserService()
    
    user = service.create_user('Bob', 'bob@example.com')
    
    assert user.name == 'Bob'
    assert user.email == 'bob@example.com'
    assert user.id == 1

def test_get_user_by_id():
    """测试获取用户"""
    service = UserService()
    service.create_user('Alice', 'alice@example.com')
    
    user = service.get_user_by_id(1)
    assert user is not None
    assert user.name == 'Alice'

def test_get_nonexistent_user():
    """测试获取不存在的用户"""
    service = UserService()
    user = service.get_user_by_id(999)
    
    assert user is None
```

### 运行特定测试

```bash
# 运行特定文件
pytest tests/test_routes/test_users.py -v

# 运行特定函数
pytest tests/test_routes/test_users.py::test_get_users -v

# 运行带标记的测试
pytest tests/ -v -m "slow"

# 显示输出
pytest tests/ -v -s

# 失败时停止
pytest tests/ -v -x

# 最后失败的测试
pytest tests/ --lf
```

### 测试覆盖率

```bash
# 安装 coverage
pip install pytest-cov

# 运行测试并生成覆盖率报告
pytest tests/ --cov=app --cov-report=term-missing

# 生成 HTML 报告
pytest tests/ --cov=app --cov-report=html

# 查看报告
open htmlcov/index.html
```

---

## 调试技巧

### 启用详细日志

```python
# 在路由中
from app import app

@app.route('/debug')
def debug_info():
    app.logger.debug("这是调试信息")
    app.logger.info("这是普通信息")
    app.logger.warning("这是警告")
    app.logger.error("这是错误")
    
    return "查看日志输出"
```

### 使用调试器

```python
# 在代码中设置断点
import pdb

@app.route('/breakpoint')
def breakpoint_test():
    pdb.set_trace()  # 程序会在这里暂停
    return "继续执行"
```

### 查看日志文件

```bash
# 实时查看日志
tail -f logs/app.log

# 查看错误日志
grep ERROR logs/app.log

# 查看最近的 100 行
tail -n 100 logs/app.log
```

---

## 最佳实践

1. **路由命名规范**：使用 `blueprint_name.endpoint_name` 格式
2. **错误处理**：统一使用 `@app.errorhandler` 处理异常
3. **输入验证**：始终验证用户输入
4. **日志记录**：关键操作都要记录日志
5. **测试覆盖**：核心功能必须有单元测试
6. **配置分离**：敏感信息使用环境变量
7. **文档更新**：添加新功能时同步更新文档

## 功能特性

- **模块化路由管理**：按功能拆分路由（main、api、admin、users 等）
- **JSON 格式结构化日志**：支持日志轮转和异常追踪
- **多环境配置支持**：开发/测试/生产环境独立配置
- **完整的测试套件**：7+ 个单元测试，覆盖率高
- **应用工厂模式**：支持灵活的应用创建和配置
- **蓝图架构**：易于扩展和维护的代码结构
- **WSGI 支持**：兼容 Gunicorn、uWSGI 等生产服务器

## 技术栈

- **Web 框架**: Flask 2.3.3
- **Python**: 3.12
- **测试**: pytest 9.0, pytest-cov
- **WSGI**: Gunicorn / uWSGI
- **模板引擎**: Jinja2 3.1
- **日志**: RotatingFileHandler (自动轮转)
