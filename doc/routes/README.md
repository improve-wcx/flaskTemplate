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
- `GET /api/apis` - 查询所有可用接口

### 管理路由 (admin.py)
- `GET /admin/` - 管理后台 (待实现)

### 文本共享路由 (text_submission.py)
- `POST /api/v1/submission` - 提交文本内容
- `POST /api/v1/submissions` - 获取文本列表（支持分页、搜索、过滤）
- `GET /api/v1/text_submission` - 文本提交页面

## 命令行客户端

所有 Web API 接口都可通过命令行客户端访问。使用方式：

```bash
# 查看所有命令
python cli.py --help

# 查询所有可用接口
python cli.py apis

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
