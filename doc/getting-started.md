# 开发者指南

> 本指南帮助开发者快速上手并了解如何添加新功能。

## 🚀 快速开始

### 环境要求

- Python 3.12+
- pip 或 poetry
- Protocol Buffers 编译器 (protoc) - 仅当使用 protobuf 时

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd projectTemplate

# 2. 创建虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac
# 或 env\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements-dev.txt

# 4. (可选) 安装 protoc 编译器
# Ubuntu/Debian: sudo apt-get install protobuf-compiler
# macOS: brew install protobuf
# 或从 https://github.com/protocolbuffers/protobuf/releases 下载
```

### 运行应用

```bash
# 开发模式（自动重载）
python run.py

# 生产模式
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 运行测试

```bash
pytest tests/ -v
```

---

## 📝 如何添加新接口

添加一个新接口需要完成以下步骤：

### 1. 创建路由文件

在 `app/routes/` 目录下创建新的路由文件：

```python
# app/routes/users.py
from flask import Blueprint, request, jsonify
from utils.logger import get_request_id

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/', methods=['GET'])
def list_users():
    """获取用户列表"""
    request_id = get_request_id()
    # 实现逻辑
    return jsonify([])
```

### 2. 注册路由

在 `app/__init__.py` 中注册新路由：

```python
def create_app(config_name=None):
    app = Flask(__name__)
    
    # 注册新路由
    from app.routes.users import users_bp
    app.register_blueprint(users_bp)
    
    return app
```

### 3. 添加 CLI 支持

在 `cli.py` 中添加对应的命令行命令：

```python
def cmd_users(args):
    """用户列表命令"""
    url = f"{args.base_url}/api/users"
    status_code, data = make_request(url)
    return print_response(status_code, data)

# 在 main() 中添加子命令
users_parser = subparsers.add_parser('users', help='用户列表')
users_parser.set_defaults(func=cmd_users)
```

### 4. 编写单元测试

在 `tests/test_routes/` 下创建测试文件：

```python
# tests/test_routes/test_users.py
import unittest
from app import create_app

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_list_users(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

### 5. 编写接口文档

在 `doc/api/` 或 `doc/routes/` 下添加文档：

```markdown
# 用户接口

## 获取用户列表

**GET** `/api/users`

### 请求参数

无

### 响应示例

```json
{
  "users": [],
  "total": 0
}
```
```

### 6. 更新主文档

- 更新 `doc/routes/README.md` 添加新路由说明
- 更新 `doc/cli/README.md` 添加新命令说明
- 更新主 `README.md`（如适用）

### 检查清单

- [ ] 路由文件已创建
- [ ] 路由已注册
- [ ] CLI 命令已添加
- [ ] 单元测试已编写（至少覆盖正常情况和异常情况）
- [ ] 接口文档已更新
- [ ] CLI 文档已更新
- [ ] 所有测试通过：`pytest tests/ -v`

---

## 📦 如何添加 Protocol Buffers

### 1. 编写 .proto 文件

在 `proto/` 目录下创建新的 proto 文件：

```protobuf
// proto/user.proto
syntax = "proto3";

package user;

message User {
  string user_id = 1;
  string username = 2;
  string email = 3;
}

message UserRequest {
  string user_id = 1;
}

message UserResponse {
  bool success = 1;
  User user = 2;
  string message = 3;
  string request_id = 4;
}
```

### 2. 编译 proto 文件

```bash
# 使用项目脚本
python scripts/generate_protobuf.py

# 或手动编译
protoc --python_out=app/proto --pyi_out=app/proto proto/user.proto
```

### 3. 在路由中使用

```python
from app.proto import user_pb2
from google.protobuf.json_format import ParseDict, MessageToDict

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    request_id = get_request_id()
    
    # 构建响应
    response_msg = user_pb2.UserResponse(
        success=True,
        message="User found",
        request_id=request_id
    )
    response_msg.user.user_id = user_id
    
    return jsonify(MessageToDict(response_msg))
```

### 4. 更新文档

在 `doc/protobuf/` 下添加说明：

```markdown
# User 消息定义

## User

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户 ID |
| username | string | 用户名 |
| email | string | 邮箱 |
```

### 检查清单

- [ ] .proto 文件已创建
- [ ] 包名已定义（避免使用 helloworld 等通用名称）
- [ ] 已编译生成 .pb2.py 和 .pb2.pyi 文件
- [ ] 路由中正确使用 ParseDict/MessageToDict
- [ ] 文档已更新

---

## 🧪 测试规范

### 测试类型

1. **单元测试** - 测试单个函数或方法
2. **集成测试** - 测试多个组件协作
3. **CLI 测试** - 测试命令行客户端

### 编写测试

```python
# tests/test_routes/test_example.py
import unittest
from app import create_app

class TestExample(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """测试后清理"""
        pass
    
    def test_success_case(self):
        """测试成功情况"""
        response = self.client.get('/api/example')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('request_id', data)
    
    def test_error_case(self):
        """测试错误情况"""
        response = self.client.get('/api/example/invalid')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_routes/test_example.py -v

# 运行特定测试
pytest tests/test_routes/test_example.py::TestExample::test_success_case -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

---

## 📚 文档规范

### 文档结构

```
doc/
├── README.md              # 文档总索引
├── getting-started.md     # 开发者指南（本文档）
├── cli/                   # CLI 文档
│   └── README.md
├── log/                   # 日志系统
│   ├── README.md
│   ├── format.md
│   └── usage.md
├── protobuf/              # Protobuf 文档
│   ├── README.md
│   └── INDEX.md
├── routes/                # 路由文档
│   ├── README.md
│   └── development.md
├── api/                   # API 文档
│   └── README.md
└── deployment/            # 部署文档
    ├── README.md
    ├── quick-start.md
    └── architecture.md
```

### 文档编写原则

1. **简明扼要** - 避免冗余，只写必要信息
2. **示例驱动** - 提供可运行的代码示例
3. **版本同步** - 确保文档与代码版本一致
4. **中文优先** - 主要文档使用中文，代码注释可用英文

### 更新文档的时机

- 添加新接口时
- 修改现有接口行为时
- 添加/修改 CLI 命令时
- 更新配置项时
- 部署流程变化时

---

## 🔧 常见问题

### Q: protoc 编译器找不到？

```bash
# Ubuntu/Debian
sudo apt-get install protobuf-compiler

# macOS
brew install protobuf

# 验证安装
protoc --version
```

### Q: 如何查看日志？

```bash
# 实时查看
tail -f logs/app.log

# 查看最近 100 行
tail -n 100 logs/app.log

# 搜索特定 request_id
grep "request-id-here" logs/app.log
```

### Q: 如何调试？

```bash
# 开启调试模式
export FLASK_ENV=development
python run.py

# 查看详细日志
python -u run.py  # 禁用输出缓冲
```

### Q: 数据库迁移？

（如使用数据库，在此说明迁移步骤）

---

## 📖 相关文档

- [CLI 使用指南](cli/README.md)
- [日志系统说明](log/README.md)
- [Protobuf 使用指南](protobuf/README.md)
- [路由开发指南](routes/development.md)
- [部署文档](deployment/README.md)
- [测试指南](testing/README.md)
