# 开发者指南

本指南帮助开发者快速上手并了解如何添加新功能。

## 🚀 快速开始

### 环境要求
- Python 3.9+
- pip
- Protocol Buffers 编译器 (protoc，仅使用 protobuf 时需要)

### 安装步骤
```bash
# 1. 克隆项目
git clone <repository-url>
cd flaskTemplate

# 2. 创建虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac
# Windows: env\Scripts\activate

# 3. 安装依赖
# 自动检测平台
python scripts/install_deps.py

# 或手动安装
# Linux/macOS: pip install -r requirements/linux.txt
# Windows: pip install -r requirements/windows.txt

# 4. 生成 Protobuf 代码 (如需要)
python scripts/generate_protobuf.py  # Linux/macOS
# Windows: python scripts\generate_protobuf_win.py
```

### 运行应用
```bash
# 开发模式
python run.py

# 生产模式
# Linux/macOS
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Windows
pip install waitress
python wsgi.py
```

### 运行测试

```bash
pytest tests/ -v
```

## 📝 添加新接口

### 1. 创建路由文件
在 `app/routes/` 创建新路由文件：

```python
# app/routes/example.py
from flask import Blueprint, jsonify
from utils.logger import get_request_id

example_bp = Blueprint('example', __name__, url_prefix='/api/example')

@example_bp.route('/', methods=['GET'])
def get_example():
    """获取示例数据"""
    request_id = get_request_id()
    return jsonify({"message": "Hello World", "request_id": request_id})
```

### 2. 注册路由
在 `app/__init__.py` 中注册蓝图：

```python
# 注册新路由
from app.routes.example import example_bp
app.register_blueprint(example_bp)
```

### 3. 添加 CLI 支持 (可选)
在 `cli.py` 中添加命令：

```python
def cmd_example(args):
    """示例命令"""
    url = f"{args.base_url}/api/example"
    status_code, data = make_request(url)
    return print_response(status_code, data)
```

### 4. 编写测试
在 `tests/test_routes/` 创建测试：

```python
# tests/test_routes/test_example.py
import unittest
from app import create_app

class TestExample(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_get_example(self):
        response = self.client.get('/api/example')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('request_id', data)
```

### 5. 更新文档
- 在 `doc/api/README.md` 添加 API 说明
- 在 `doc/cli/README.md` 添加 CLI 命令说明

### 检查清单
- [ ] 路由文件已创建
- [ ] 路由已注册
- [ ] 测试已编写 (`pytest tests/ -v`)
- [ ] 文档已更新

## 📦 添加 Protocol Buffers

### 1. 创建 .proto 文件
在 `proto/` 目录创建 proto 文件：

```protobuf
// proto/example.proto
syntax = "proto3";

package example;

message ExampleMessage {
  string content = 1;
  string request_id = 2;
}
```

### 2. 生成 Python 代码
```bash
# Linux/macOS
python scripts/generate_protobuf.py

# Windows
python scripts\generate_protobuf_win.py
```

### 3. 在路由中使用
```python
from app.proto import example_pb2
from google.protobuf.json_format import MessageToDict

@example_bp.route('/', methods=['POST'])
def create_example():
    request_msg = example_pb2.ExampleMessage()
    # 使用 request_msg...
    return jsonify(MessageToDict(response_msg))
```

## 🧪 测试规范

### 编写测试
```python
# tests/test_routes/test_example.py
import unittest
from app import create_app

class TestExample(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_success(self):
        response = self.client.get('/api/example')
        self.assertEqual(response.status_code, 200)
    
    def test_error(self):
        response = self.client.get('/api/example/invalid')
        self.assertEqual(response.status_code, 404)
```

### 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_routes/test_example.py -v

# 生成覆盖率
pytest tests/ --cov=app --cov-report=html
```

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

## 📚 文档规范

### 文档结构
```
doc/
├── README.md              # 文档索引
├── getting-started.md     # 开发者指南（本文件）
├── QUICK_REFERENCE.md     # 快速命令参考
├── api/                   # API 文档
├── cli/                   # CLI 文档
├── routes/                # 路由文档
├── testing/               # 测试文档
└── deployment/            # 部署文档
```

### 编写原则
- **简明扼要**: 避免冗余，只写必要信息
- **示例驱动**: 提供可运行的代码示例
- **版本同步**: 确保文档与代码版本一致

### 更新时机
- 添加新接口时
- 修改接口行为时
- 添加/修改 CLI 命令时
- 部署流程变化时

## 🔧 常见问题

### Protobuf 编译失败
```bash
# 安装 protoc
# Ubuntu/Debian
sudo apt-get install protobuf-compiler

# macOS
brew install protobuf

# 验证安装
protoc --version
```

### 虚拟环境问题
```bash
# 删除并重新创建
rm -rf env
python3 -m venv env
source env/bin/activate
pip install -r requirements/dev.txt
```

### 端口被占用
修改 `config/config.json` 中的 `port` 配置项。
    
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
