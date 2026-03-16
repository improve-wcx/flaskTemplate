# 项目文档索引

> 完整的项目文档，涵盖开发、部署、API 使用等各个方面。

## 📚 文档结构

```
doc/
├── README.md              # 本文档 - 总索引
├── getting-started.md     # 🚀 开发者指南（新增）
├── cli/                   # 命令行客户端
│   └── README.md
├── log/                   # 日志系统
│   ├── README.md
│   ├── format.md
│   ├── usage.md
│   └── architecture.md
├── protobuf/              # Protocol Buffers
│   ├── README.md
│   └── INDEX.md
├── routes/                # 路由模块
│   ├── README.md
│   └── development.md
├── api/                   # API 接口
│   └── README.md
├── deployment/            # 部署文档
│   └── README.md
├── testing/               # 测试
│   └── README.md
├── models/                # 数据模型
│   └── README.md
└── services/              # 业务逻辑
    └── README.md
```

## 🎯 快速导航

### 新手入门

1. **[开发者指南](getting-started.md)** ⭐ 必读
   - 如何添加新接口
   - 如何添加 Protobuf
   - 测试规范
   - 文档规范

2. **[快速部署](deployment/README.md)**
   - 开发环境设置
   - 生产环境部署
   - Protobuf 编译

### 核心功能

- **[CLI 使用指南](cli/README.md)** - 命令行客户端
- **[日志系统](log/README.md)** - 结构化日志和 Request ID
- **[Protobuf 指南](protobuf/README.md)** - 数据序列化
- **[路由开发](routes/README.md)** - 添加和修改路由
- **[文本共享](api/README.md#文本共享-api)** - 富文本提交和展示系统

### 进阶主题

- **[API 设计](api/README.md)** - RESTful API 规范
- **[测试指南](testing/README.md)** - 单元测试编写
- **[数据模型](models/README.md)** - 模型设计
- **[服务层](services/README.md)** - 业务逻辑实现

## 📖 文档阅读顺序

### 新开发者

1. 开发者指南
2. 快速部署
3. CLI 使用
4. 路由开发
5. Protobuf 指南
6. 测试指南

### 添加新功能

1. 开发者指南
2. 添加接口流程
3. 编写测试
4. 更新文档

## 🔍 按主题查找

### 开发相关

- **添加接口**: [开发者指南 - 如何添加新接口](getting-started.md#如何添加新接口)
- **添加 Protobuf**: [开发者指南 - 如何添加 Protocol Buffers](getting-started.md#如何添加-protocol-buffers)
- **路由开发**: [路由开发指南](routes/development.md)
- **API 设计**: [API 文档](api/README.md)

### 部署相关

- **环境设置**: [部署指南 - 开发环境](deployment/README.md#开发环境设置)
- **生产部署**: [部署指南 - 生产环境](deployment/README.md#生产环境部署)
- **Protobuf 编译**: [部署指南 - Protobuf 编译](deployment/README.md#protobuf-编译)
- **故障排查**: [部署指南 - 故障排查](deployment/README.md#故障排查)

### 测试相关

- **测试编写**: [开发者指南 - 测试规范](getting-started.md#测试规范)
- **测试运行**: [测试指南](testing/README.md)

### 工具使用

- **CLI 客户端**: [CLI 使用指南](cli/README.md)
- **日志查看**: [日志系统](log/README.md)
- **Protobuf**: [Protobuf 指南](protobuf/README.md)

## 📝 文档维护

### 何时更新文档

- ✅ 添加新接口时
- ✅ 修改现有接口行为时
- ✅ 添加/修改 CLI 命令时
- ✅ 更新配置项时
- ✅ 部署流程变化时
- ✅ 发现文档错误时

### 文档质量检查

- [ ] 内容准确无误
- [ ] 示例代码可运行
- [ ] 链接正确有效
- [ ] 语言简明扼要
- [ ] 与代码版本同步

## 🤝 贡献文档

1. 找到相关文档文件
2. 使用 Markdown 格式
3. 添加清晰的标题和示例
4. 提交 Pull Request

## 📞 问题反馈

如发现文档问题或需要补充内容，请：
1. 创建 Issue 描述问题
2. 或直接提交 PR 修复

---

**最后更新**: 2026-03-16
