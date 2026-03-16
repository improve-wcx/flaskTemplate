# Flask Project Template

一个结构化的 Flask 项目模板，支持模块化开发和多环境配置。

## 🌍 跨平台支持

本项目支持以下平台：

| 平台 | Python 版本 | WSGI 服务器 | 状态 |
|------|------------|-----------|------|
| **Windows** | 3.9+ | Waitress | ✅ 生产就绪 |
| **Ubuntu/Linux** | 3.9+ | Gunicorn | ✅ 生产就绪 |
| **macOS** | 3.9+ | Gunicorn | ✅ 测试通过 |

---

## 🚀 快速开始

### 方式一：自动安装（推荐）

```bash
# Windows
python scripts\install_deps.py

# Linux/macOS
python scripts/install_deps.py
```

### 方式二：手动安装

#### Windows

```bash
# 1. 创建虚拟环境
py -m venv env
.\env\Scripts\Activate.ps1

# 2. 安装依赖
pip install -r requirements\windows.txt

# 3. 生成 Protobuf 代码
python scripts\generate_protobuf_win.py

# 4. 运行测试
pytest tests/ -v

# 5. 启动服务
python run.py
```

#### Linux/Ubuntu

```bash
# 1. 创建虚拟环境
python3 -m venv env
source env/bin/activate

# 2. 安装依赖
pip install -r requirements/linux.txt

# 3. 生成 Protobuf 代码
python scripts/generate_protobuf.py

# 4. 运行测试
pytest tests/ -v

# 5. 启动服务
python run.py
```

### 使用 Make 命令

#### Windows (PowerShell)
```powershell
.\make.ps1 install-dev    # 安装开发依赖
.\make.ps1 protobuf       # 生成 Protobuf 代码
.\make.ps1 test           # 运行测试
.\make.ps1 run            # 启动服务
```

#### Linux/macOS
```bash
make install-dev          # 安装开发依赖
make protobuf             # 生成 Protobuf 代码
make test                 # 运行测试
make run                  # 启动服务
```

---

## ✨ 项目特点

- **JSON 配置** - 统一管理所有环境配置
- **模块化路由** - 按功能拆分路由模块
- **结构化日志** - JSON 格式日志输出，支持 request_id 追踪
- **完整测试** - 48+ 单元测试覆盖
- **动态 API 注册** - 自动收集和分类所有 API 端点
- **应用工厂** - 灵活的应用创建模式
- **Protocol Buffers** - 支持 protobuf 数据序列化
- **命令行客户端** - 所有 API 接口均可通过 CLI 调用
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
