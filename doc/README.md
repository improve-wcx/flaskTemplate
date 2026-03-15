# 项目文档索引

## 目录结构

```
doc/
├── api/           # API 接口文档
├── routes/        # 路由模块文档
├── models/        # 数据模型文档
├── services/      # 业务逻辑层文档
├── deployment/    # 部署文档
└── testing/       # 测试文档
```

## 快速导航

- [部署指南](deployment/README.md) - 如何运行和部署项目
- [路由开发](routes/README.md) - 如何添加和修改路由
- [API 设计](api/README.md) - API 接口规范
- [数据模型](models/README.md) - 数据模型设计
- [业务逻辑](services/README.md) - 服务层开发
- [单元测试](testing/README.md) - 测试编写指南

## 开发者指南

### 新开发者入门
1. 阅读 [部署/快速开始](deployment/quick-start.md)
2. 了解项目 [架构说明](deployment/architecture.md)
3. 查看 [路由开发指南](routes/development.md)

### 拓展模块
- 添加新路由 → 参考 `routes/development.md`
- 添加新 API → 参考 `api/development.md`
- 添加数据模型 → 参考 `models/development.md`
- 添加业务逻辑 → 参考 `services/development.md`

### 配置管理
- 查看 [配置系统文档](deployment/configuration.md)
