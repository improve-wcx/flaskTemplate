# 路由模块说明

## 概述

本项目提供多种类型的路由接口，包括主路由、API 路由、管理路由和 Protobuf 演示接口。所有接口均可通过 Web API 或命令行客户端访问。

## 现有路由

### 主路由 (main.py)
- `GET /` - 首页
- `GET /favicon.ico` - 返回 204

### API 路由 (api.py)
- `GET /api/health` - 健康检查
- `GET /api/version` - 版本信息

### 管理路由 (admin.py)
- `GET /admin/` - 管理后台 (待实现)

### Protobuf 演示路由 (demo_protobuf.py)
- `GET /api/v1/demo/hello` - 简单问候 (GET)
- `POST /api/v1/demo/hello` - 带参数的问候 (POST)
- `GET /api/v1/demo/user/<user_id>` - 获取用户信息
- `POST /api/v1/demo/users` - 获取用户列表
- `POST /api/v1/demo/echo` - Echo 接口

## 命令行客户端

所有 Web API 接口都可通过命令行客户端访问。使用方式：

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

# Echo 接口
python cli.py echo --data '{"key": "value"}'

# 指定服务器地址
python cli.py -b http://localhost:5000 health
```

详细使用说明请参考：[命令行客户端指南](../cli/README.md)

## 开发文档

详细开发指南请参考：[路由开发指南](development.md)
