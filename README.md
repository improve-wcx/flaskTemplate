# Flask 项目模板

一个结构化的 Flask Web 应用模板，支持跨平台开发和模块化架构。

## ✨ 项目特性

- **🔧 模块化架构** - 按功能拆分的路由和服务模块
- **📊 结构化日志** - JSON 格式日志，支持请求追踪
- **🧪 完整测试** - 48+ 单元测试覆盖核心功能
- **📡 动态 API 注册** - 自动收集和分类所有 API 端点
- **🏭 应用工厂模式** - 灵活的应用创建和配置
- **📋 Protocol Buffers** - 高性能数据序列化支持
- **💻 命令行客户端** - 完整的 CLI 接口支持
- **🌍 跨平台兼容** - Windows/Linux/macOS 无缝切换
- **📝 富文本共享** - 完整的文本提交和展示系统

## 🚀 快速开始

### 环境要求

- **Python**: 3.9+
- **操作系统**: Windows 10+ / Ubuntu 18.04+ / macOS 10.15+

### 自动安装（推荐）

```bash
# 自动检测平台并安装依赖
python scripts/install_deps.py
```

### 手动安装

#### Windows
```powershell
# 1. 创建虚拟环境
py -m venv env
.\env\Scripts\Activate.ps1

# 2. 安装依赖（完整开发环境）
pip install -r requirements/windows.txt

# 3. 运行测试
pytest tests/ -v

# 4. 启动服务
python run.py
```

#### Linux/macOS
```bash
# 1. 创建虚拟环境
python3 -m venv env
source env/bin/activate

# 2. 安装依赖（完整开发环境）
pip install -r requirements/linux.txt

# 3. 运行测试
pytest tests/ -v

# 4. 启动服务
python run.py
```

## 📱 使用说明

### 开发服务器

启动开发服务器：`http://127.0.0.1:5000`

```bash
python run.py
```

### 核心接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /` | GET | 首页，展示功能导航 |
| `GET /api/health` | GET | 健康检查，返回服务状态 |
| `GET /api/version` | GET | 返回当前 API 版本 |
| `GET /api/apis` | GET | 列出已注册的所有 API（通过 `register_api`） |
| `GET /relationship-map` | GET | 关系图页面（静态 HTML） |
| `POST /api/v1/submission` | POST | 提交文本内容（富文本共享） |
| `POST /api/v1/submissions` | POST | 分页获取已提交的文本列表 |
| `GET /api/v1/text_submission` | GET | 渲染文本提交页面 |

### 命令行客户端

```bash
# 查看帮助
python cli.py --help

# 健康检查
python cli.py health

# 查看已注册的 API 列表
python cli.py apis

# 文本提交示例
python cli.py text-submit --content "Hello World"
```
<!-- The Protocol Buffers demo has been removed from the project. -->
# 类型检查
mypy app/
```

### 测试运行

```bash
# 运行所有测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

## 📦 项目结构

```
flaskTemplate/
├── app/                    # 应用核心
│   ├── __init__.py        # 应用工厂
│   ├── routes/            # 路由模块
│   ├── services/          # 业务逻辑
│   ├── models/            # 数据模型
│   └── proto/             # Protobuf 定义
├── config/                 # 配置管理
├── tests/                  # 测试用例
├── scripts/                # 构建脚本
├── requirements/           # 依赖管理
├── doc/                    # 项目文档
└── logs/                   # 日志文件
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！请先阅读：

- [贡献指南](CONTRIBUTING.md)
- [编码规范](CODING_STANDARDS.md)

## 📄 许可证

MIT License
- **跨平台支持** - Windows/Linux/macOS 无缝切换

---

## 📦 依赖管理

本项目采用**分层依赖管理**方案，将依赖按功能和平台拆分：

```
requirements/
├── base.txt          # 基础依赖（所有平台通用）
├── test.txt          # 测试依赖（所有平台通用）
├── dev.txt           # 开发工具（所有平台通用）
├── linux.txt         # Linux 平台完整依赖
├── windows.txt       # Windows 平台完整依赖
├── prod.txt          # 生产环境依赖
└── dev.txt           # 开发环境依赖
```

### 依赖文件说明

| 文件 | 说明 | 包含 |
|------|------|------|
| `base.txt` | 核心框架 | Flask, protobuf |
| `test.txt` | 测试工具 | pytest, pytest-cov |
| `dev.txt` | 开发工具 | python-dotenv |
| `linux.txt` | Linux 完整依赖 | base + test + dev + gunicorn |
| `windows.txt` | Windows 完整依赖 | base + test + dev + waitress + colorama |

### 安装方式

```bash
# 安装完整开发环境（推荐）
# Windows
pip install -r requirements/windows.txt

# Linux
pip install -r requirements/linux.txt

# 仅安装基础依赖
pip install -r requirements/base.txt

# 仅安装测试依赖
pip install -r requirements/test.txt
```

---

## 🛠️ 如何添加新接口

添加一个新接口需要完成以下步骤：

### 1. 创建路由文件
在 `app/routes/` 创建新文件（如 `app/routes/users.py`）

### 2. 注册路由
在 `app/__init__.py` 中注册新蓝图，并指定分类（如 `系统`, `用户管理` 等）。路由会自动被 `/apis` 端点收集和分类。

### 3. 添加 CLI 支持
在 `cli.py` 中添加对应的命令行命令

### 4. 编写单元测试
在 `tests/test_routes/` 创建测试文件

### 5. 更新文档
- `doc/routes/README.md` - 添加路由说明
- `doc/cli/README.md` - 添加 CLI 命令说明
- 可选：在 `doc/api/` 添加详细 API 文档

**详细说明**: [开发者指南 - 如何添加新接口](doc/getting-started.md#如何添加新接口)

---

## 📱 命令行客户端

所有 Web API 接口都可通过命令行客户端访问：

```bash
# 查看所有命令
python cli.py --help

# 健康检查
python cli.py health

# 问候接口
python cli.py hello --get
python cli.py hello --post --name "Alice"

# 用户接口
python cli.py user 12345
python cli.py users --page 1 --page-size 10

# 查询所有可用接口
python cli.py apis

# Echo 测试
python cli.py echo --data '{"key": "value"}'
```

详细使用说明请参考：[命令行客户端指南](doc/cli/README.md)

---

## 📄 示例接口

项目包含一个 **Protocol Buffers 演示** (`/api/v1/demo`)，展示如何在 Flask 中使用 protobuf：

### GET 示例
```bash
# 简单问候
curl http://localhost:5000/api/v1/demo/hello

# 获取用户
curl http://localhost:5000/api/v1/demo/user/12345
```

### POST 示例
```bash
# 带参数的问候
curl -X POST http://localhost:5000/api/v1/demo/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# 获取用户列表
curl -X POST http://localhost:5000/api/v1/demo/users \
  -H "Content-Type: application/json" \
  -d '{"page": 1, "page_size": 10}'
```

---

## 📚 文档

详细文档请查看 [doc/](doc/) 目录：

### 核心文档

- **[开发者指南](doc/getting-started.md)** ⭐ 必读 - 如何添加接口、测试规范等
- **[部署指南](doc/deployment/README.md)** - 运行和部署说明
- **[CLI 使用指南](doc/cli/README.md)** - 命令行客户端详解
- **[路由开发](doc/routes/development.md)** - 如何添加路由
- **[Protobuf 指南](doc/protobuf/README.md)** - 数据序列化说明

### 其他文档

- [日志系统](doc/log/README.md) - 日志格式和使用
- [API 设计](doc/api/README.md) - API 设计规范
- [测试指南](doc/testing/README.md) - 编写单元测试
- [项目架构](doc/architecture.md) - 架构说明
- [数据模型](doc/models/README.md) - 数据模型说明
- [服务层](doc/services/README.md) - 业务逻辑层说明

---

## 🔧 开发环境配置

### Python 版本要求

- **最低版本**: Python 3.9
- **推荐版本**: Python 3.9 - 3.12

### 虚拟环境

#### Windows
```powershell
py -m venv env
.\env\Scripts\Activate.ps1
```

#### Linux/macOS
```bash
python3 -m venv env
source env/bin/activate
```

### 常用开发命令

```bash
# 运行测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=app -v

# 格式化代码
# 建议安装 black: pip install black
black app/ tests/

# 静态类型检查
# 建议安装 mypy: pip install mypy
mypy app/

# 清理临时文件
# Windows
.\make.ps1 clean

# Linux/macOS
make clean
```

---

## 🌐 访问应用

开发服务器运行在：`http://127.0.0.1:5000`

### 可用端点

#### 系统接口
- `GET /` - 首页
- `GET /api/health` - 健康检查
- `GET /api/version` - 版本信息
- `GET /api/apis` - 列出所有 API

#### Protobuf 演示
- `GET /api/v1/demo/hello` - 获取问候
- `POST /api/v1/demo/hello` - 发送问候
- `GET /api/v1/demo/user/{user_id}` - 获取用户
- `POST /api/v1/demo/users` - 获取用户列表

---

## 🐳 生产部署

### Windows

```bash
# 安装 Waitress
pip install waitress

# 运行生产服务器
python wsgi.py
```

### Linux

```bash
# 安装 Gunicorn
pip install gunicorn

# 运行生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

详细部署说明请参考：[部署指南](doc/deployment/README.md)

---

## ❓ 常见问题

### Q: 如何切换 Python 版本？
A: 删除 `env/` 目录，使用新 Python 版本重新创建虚拟环境：
```bash
# Windows
py -m venv env
.\env\Scripts\Activate.ps1

# Linux
python3.12 -m venv env
source env/bin/activate
```

### Q: Protobuf 代码生成失败？
A: 
- Windows: 使用 `python scripts\generate_protobuf_win.py`
- Linux: 确保已安装 `protoc` 和 `grpcio-tools`

### Q: 端口 5000 被占用？
A: 修改 `config/config.json` 中的 `port` 配置

### Q: 如何查看日志？
A: 日志文件位于 `logs/` 目录：
- `app.log` - 应用日志
- `trace.log` - 请求追踪日志

---

## 📝 更新日志

### v2.0.0 (2026-03-16)
- ✨ 新增跨平台依赖管理方案
- ✨ 新增自动平台检测安装脚本
- ✨ 新增 Windows PowerShell Makefile
- ✨ 优化依赖文件结构（分层管理）
- 🐛 修复 pytest 版本冲突问题
- 🐛 修复 Windows 下 Protobuf 生成问题

### v1.0.0
- 初始版本发布
- 支持 Ubuntu/Linux 平台

---

## 📄 许可证

MIT License
