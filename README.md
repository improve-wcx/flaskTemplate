# Flask Project Template

一个结构化的 Flask 项目模板，支持模块化开发和多环境配置。

## 快速开始

### 1. 安装依赖

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements-dev.txt
```

### 2. 运行应用

```bash
# 开发模式
python run.py

# 生产模式
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 3. 运行测试

```bash
pytest tests/ -v
```

## 项目特点

- **JSON 配置** - 统一管理所有环境配置
- **模块化路由** - 按功能拆分路由模块
- **结构化日志** - JSON 格式日志输出，支持 request_id 追踪
- **完整测试** - 25+ 单元测试覆盖
- **应用工厂** - 灵活的应用创建模式
- **Protocol Buffers** - 支持 protobuf 数据序列化
- **命令行客户端** - 所有 API 接口均可通过 CLI 调用

## 命令行客户端

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

# Echo 测试
python cli.py echo --data '{"key": "value"}'
```

详细使用说明请参考：[命令行客户端指南](doc/cli/README.md)

## 示例接口

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

## 文档

详细文档请查看 [doc/](doc/) 目录：

- [部署指南](doc/deployment/README.md) - 运行和部署说明
- [路由开发](doc/routes/development.md) - 如何添加路由
- [API 设计](doc/api/README.md) - API 设计规范
- [测试指南](doc/testing/README.md) - 编写单元测试
- [项目架构](doc/deployment/architecture.md) - 架构说明
- [日志系统](doc/log/README.md) - 日志格式和使用
- [Protocol Buffers](doc/protobuf/README.md) - protobuf 使用指南

## 技术栈

- Flask 2.3.3
- Python 3.12
- pytest 9.0
- Gunicorn
- Protocol Buffers

## 项目结构

```
projectTemplate/
├── app/
│   ├── routes/
│   │   └── demo_protobuf.py    # Protobuf 演示接口
│   ├── services/
│   └── models/
├── proto/                       # Proto 文件
│   ├── helloworld.proto
│   └── common.proto
├── tests/                       # 测试
├── doc/                         # 文档
└── logs/                        # 日志文件
```
