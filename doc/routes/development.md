# 路由开发指南

## 路由模块结构

```
app/routes/
├── __init__.py
├── main.py      # 主路由
├── api.py       # API 路由
└── admin.py     # 管理路由
```

## 创建新路由

### 步骤 1: 创建路由文件

```python
# app/routes/users.py
from flask import Blueprint, jsonify, request

# 创建蓝图
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/')
def get_users():
    """获取所有用户"""
    return jsonify([])

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    """获取指定用户"""
    return jsonify({'id': user_id})
```

### 步骤 2: 注册蓝图

```python
# app/__init__.py
def create_app(config_name=None):
    app = Flask(__name__)
    
    # 导入并注册新路由
    from app.routes.users import users_bp
    app.register_blueprint(users_bp)
    
    return app
```

### 步骤 3: 测试

```bash
curl http://127.0.0.1:5000/api/users/
curl http://127.0.0.1:5000/api/users/1
```

## 路由类型

### 1. RESTful API 路由

```python
@users_bp.route('/', methods=['GET'])
def list_users():
    """列出所有用户"""
    pass

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    """获取单个用户"""
    pass

@users_bp.route('/', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.get_json()
    pass

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    """更新用户"""
    pass

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    """删除用户"""
    pass
```

### 2. Web 页面路由

```python
from flask import render_template

@pages_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html', title='关于')
```

### 3. 静态文件路由

```python
@app.route('/download/<filename>')
def download_file(filename):
    """下载文件"""
    return send_from_directory('downloads', filename)
```

## 路由参数

### 类型转换器

```python
@users_bp.route('/<int:user_id>')      # 整数
@users_bp.route('/<string:username>')  # 字符串
@users_bp.route('/<float:price>')      # 浮点数
@users_bp.route('/<uuid:id>')          # UUID
@users_bp.route('/<path:filepath>')    # 路径
```

### 多个参数

```python
@orders_bp.route('/users/<int:user_id>/orders/<int:order_id>')
def get_user_order(user_id, order_id):
    """获取用户的订单"""
    pass
```

## 请求处理

### 获取请求数据

```python
from flask import request

# JSON 数据
data = request.get_json()

# 查询参数
page = request.args.get('page', 1, type=int)

# 表单数据
name = request.form.get('name')

# 请求头
auth = request.headers.get('Authorization')

# 请求方法
method = request.method
```

### 返回响应

```python
from flask import jsonify, make_response

# JSON 响应
return jsonify({'status': 'success'})

# 带状态码
return jsonify({'error': 'Not found'}), 404

# 自定义响应
response = make_response('Hello', 200)
response.headers['X-Custom'] = 'value'
return response
```

## 错误处理

### 路由内错误处理

```python
@users_bp.route('/<int:id>')
def get_user(id):
    user = find_user(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)
```

### 全局错误处理

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal error'}), 500
```

## 路由装饰器

### 自定义装饰器

```python
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/profile')
@login_required
def profile():
    return jsonify({'user': current_user})
```

## 最佳实践

1. **使用蓝图** - 按功能模块组织路由
2. **统一前缀** - API 路由使用 `/api/` 前缀
3. **RESTful 规范** - 遵循 REST 设计原则
4. **文档注释** - 每个路由添加 docstring
5. **输入验证** - 验证所有用户输入
6. **错误处理** - 统一错误响应格式
7. **日志记录** - 关键操作记录日志

## 示例：完整用户路由

```python
# app/routes/users.py
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

users_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

@users_bp.route('/')
def list_users():
    """
    获取所有用户列表
    ---
    responses:
      200:
        description: 用户列表
    """
    users = user_service.get_all_users()
    return jsonify([u.to_dict() for u in users])

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    """获取指定用户"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@users_bp.route('/', methods=['POST'])
def create_user():
    """创建新用户"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    user = user_service.create_user(data['name'], data.get('email', ''))
    return jsonify(user.to_dict()), 201
```
