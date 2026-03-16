# Python 编码规范

本项目遵循行业标准 Python 开发规范，确保代码质量和一致性。

## 代码格式

### Black 代码格式化
- **行长度**: 88 字符
- **字符串引号**: 优先使用双引号
- **尾随逗号**: 是，便于 diff 查看
- **自动格式化**: 所有 Python 代码必须使用 Black 格式化

### isort 导入排序
- **配置**: Black 兼容模式
- **分组**: 标准库、三方库、本地模块
- **行长度**: 88 字符
- **多行导入**: 使用括号换行

### flake8 代码检查
- **最大行长**: 88 字符
- **忽略规则**:
  - E203: Black 兼容性（冒号前空格）
  - W503: Black 兼容性（二元运算符换行）
- **额外检查**:
  - flake8-docstrings: 文档字符串规范
  - flake8-bugbear: 额外错误检测

### mypy 类型检查
- **严格模式**: 新代码启用
- **类型覆盖**: 应用代码目标 100%
- **排除目录**: tests/ 和 docs/

## 开发工作流

### 预提交钩子
所有开发者必须安装和使用预提交钩子：

```bash
pip install pre-commit
pre-commit install
```

提交时自动运行：
- 代码格式化 (Black)
- 导入排序 (isort)
- 代码检查 (flake8)
- 类型检查 (mypy)
- 文件检查

### 测试
- **框架**: pytest
- **覆盖率**: 最低 80% 要求
- **组织**: 测试镜像源码结构
- **命名**: `test_*.py` 文件，`test_*` 函数

### 日志
- **禁止使用 `print()`** 在生产代码中
- 使用 `utils/logger.py` 提供的结构化日志
- 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
- 在日志中包含相关上下文

## 项目结构

### Flask 应用结构
```
app/
├── __init__.py          # 应用工厂
├── models/              # 数据模型
├── routes/              # 路由蓝图
├── services/            # 业务逻辑服务
├── templates/           # Jinja2 模板
└── static/              # 静态资源
```

### 核心原则
- **关注点分离**: 路由处理 HTTP，服务处理业务逻辑
- **蓝图组织**: 相关路由分组到蓝图中
- **服务层**: 业务逻辑抽象到服务中
- **配置管理**: 环境-based 配置

## 代码质量准则

### 通用
- 编写自描述代码，使用清晰的变量名
- 为所有公共函数、类、模块添加文档字符串
- 保持函数简短，专注于单一职责
- 为函数参数和返回值添加类型提示

### 错误处理
- 使用具体的异常类型，不使用通用 `Exception`
- 使用适当的上下文记录错误
- 不在生产环境中向用户暴露内部错误

### 安全
- 验证所有用户输入
- 对数据库操作使用参数化查询
- 安全存储敏感数据（环境变量）
- 遵循 OWASP Web 安全指南

### 性能
- 避免 N+1 查询问题
- 使用适当的数据结构
- 在有益时缓存昂贵操作
- 在优化前分析代码

## Git 工作流

### 分支策略
- `main`: 生产就绪代码
- `develop`: 集成分支
- 功能分支: `feature/REQ-XXX-描述`
- 错误修复: `fix/问题描述`

### 提交信息
- 使用祈使语气: "添加功能" 而不是 "添加了功能"
- 第一行不超过 50 字符
- 引用问题编号: `REQ-002: 实现文本提交系统`
- 保持描述性但简洁

### Pull Request
- 所有更改需要审查
- CI/CD 必须通过（测试、检查、格式化）
- 包含更改描述和测试完成情况
- 合并时压缩提交

## 文档

### 代码文档
- 所有公共 API 必须有文档字符串
- 包含参数类型和描述
- 记录可能引发的异常
- 更改 API 时更新文档字符串

### 项目文档
- 保持 README.md 最新
- 为重大更改记录迁移指南
- 维护 API 文档
- 为发布更新变更日志

## 工具

### 必需工具
- Python 3.9+
- pip 包管理
- 虚拟环境 (venv, virtualenv, conda)
- Git 版本控制

### 推荐 IDE 设置
- VS Code + Python 扩展
- Pylance 类型检查
- Black Formatter 扩展
- isort 导入排序扩展

### CI/CD
- 推送时自动测试
- 代码质量检查（检查、格式化）
- 安全扫描
- 部署自动化

## 执行

这些规范通过以下方式强制执行：
- 预提交钩子（自动）
- CI/CD 流水线检查
- 代码审查要求
- 定期代码质量审计

违反将在开发过程中被捕获，必须在合并前修复。
- **Framework**: pytest
- **Coverage**: Minimum 80% code coverage required
- **Test Organization**: Tests mirror source code structure
- **Naming**: `test_*.py` files with `test_*` functions

### Logging
- **Never use `print()` statements** in production code
- Use the structured logging system provided in `utils/logger.py`
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include relevant context in log messages

## Project Structure

### Flask Application Structure
```
app/
├── __init__.py          # Application factory
├── models/              # Data models
├── routes/              # Route blueprints
├── services/            # Business logic services
├── templates/           # Jinja2 templates
└── static/              # Static assets (CSS, JS, images)
```

### Key Principles
- **Separation of Concerns**: Routes handle HTTP, services handle business logic
- **Blueprint Organization**: Related routes grouped in blueprints
- **Service Layer**: Business logic abstracted into services
- **Configuration Management**: Environment-based configuration

## Code Quality Guidelines

### General
- Write self-documenting code with clear variable names
- Add docstrings to all public functions, classes, and modules
- Keep functions small and focused on single responsibility
- Use type hints for function parameters and return values

### Error Handling
- Use specific exception types, not generic `Exception`
- Log errors with appropriate context
- Don't expose internal errors to users in production

### Security
- Validate all user inputs
- Use parameterized queries for database operations
- Store sensitive data securely (environment variables)
- Follow OWASP guidelines for web security

### Performance
- Avoid N+1 query problems
- Use appropriate data structures
- Cache expensive operations when beneficial
- Profile code before optimizing

## Git Workflow

### Branching Strategy
- `main`: Production-ready code
- `develop`: Integration branch
- Feature branches: `feature/REQ-XXX-description`
- Bug fixes: `fix/issue-description`

### Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 50 characters
- Reference issue numbers: `REQ-002: Implement text submission system`
- Be descriptive but concise

### Pull Requests
- All changes require review
- CI/CD must pass (tests, linting, formatting)
- Include description of changes and testing done
- Squash commits when merging

## Documentation

### Code Documentation
- All public APIs must have docstrings
- Include type hints for parameters and return values
- Document exceptions that may be raised
- Update documentation when changing APIs

### Project Documentation
- Keep README.md up to date
- Document setup and deployment procedures
- Maintain API documentation
- Update changelog for releases

## Tooling

### Required Tools
- Python 3.9+
- pip for package management
- Virtual environment (venv)
- Git for version control

### Recommended IDE Setup
- VS Code with Python extension
- Pylance for type checking
- Black Formatter extension
- isort extension for import sorting

### CI/CD
- Automated testing on push/PR
- Code quality checks (linting, formatting)
- Security scanning
- Deployment automation

## Enforcement

These standards are enforced through:
- Pre-commit hooks (automatic)
- CI/CD pipeline checks
- Code review requirements
- Regular code quality audits

Violations will be caught during development and must be fixed before merging.