# 项目文档索引

## 目录结构

```
doc/
├── README.md              # 本文档 - 项目文档总索引
├── log/                   # 日志系统文档
│   ├── README.md          # 日志系统总览
│   ├── format.md          # 日志格式规范
│   ├── usage.md           # 使用方法指南
│   ├── request_id.md      # Request ID 追踪详解
│   ├── architecture.md    # 架构设计
│   └── REQUEST_ID_GUIDE.md # Request ID 使用指南 (详细版)
├── protobuf/              # Protocol Buffers 文档
│   ├── INDEX.md           # Protocol Buffers 总览
│   └── README.md          # 使用指南 (详细版)
├── api/                   # API 接口文档
├── routes/                # 路由模块文档
├── models/                # 数据模型文档
├── services/              # 业务逻辑层文档
├── deployment/            # 部署文档
└── testing/               # 测试文档
```

## 快速导航

### 核心文档
- [📋 日志系统文档](log/README.md) - 日志格式、使用方法和 Request ID 追踪
- [🔧 Protocol Buffers 文档](protobuf/INDEX.md) - 使用 protobuf 定义数据结构
- [🚀 部署指南](deployment/README.md) - 如何运行和部署项目
- [🛣️ 路由开发](routes/README.md) - 如何添加和修改路由
- [🔌 API 设计](api/README.md) - API 接口规范
- [📊 数据模型](models/README.md) - 数据模型设计
- [⚙️ 业务逻辑](services/README.md) - 服务层开发
- [🧪 单元测试](testing/README.md) - 测试编写指南

## 开发者指南

### 新开发者入门
1. 阅读 [部署/快速开始](deployment/quick-start.md)
2. 了解项目 [架构说明](deployment/architecture.md)
3. 查看 [路由开发指南](routes/development.md)
4. 了解 [日志系统](log/README.md) - 如何查看和分析日志
5. 学习 [Protocol Buffers](protobuf/INDEX.md) - 数据序列化方式

### 拓展模块
- 添加新路由 → 参考 `routes/development.md`
- 添加新 API → 参考 `api/development.md`
- 添加数据模型 → 参考 `models/development.md`
- 添加业务逻辑 → 参考 `services/development.md`

### 配置管理
- 查看 [配置系统文档](deployment/configuration.md)
