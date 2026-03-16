# 贡献指南

感谢您对 Flask 项目模板的兴趣！本指南提供贡献者的规范和信息。

## 开发环境设置

### 环境要求
- Python 3.9+
- Git
- 虚拟环境工具 (venv, virtualenv, 或 conda)

### 初始设置
1. Fork 并克隆仓库：
   ```bash
   git clone https://github.com/your-username/flask-template.git
   cd flask-template
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv env
   # Windows:
   env\Scripts\activate
   # Linux/macOS:
   source env/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements/base.txt
   pip install -r requirements/dev.txt
   ```

4. 安装预提交钩子：
   ```bash
   pre-commit install
   ```

5. 运行初始检查：
   ```bash
   pre-commit run --all-files
   ```

## 开发工作流

### 1. 选择 Issue
- 查看 [Issues](../../issues) 页面寻找开放任务
- 寻找标记为 `good first issue` 或 `help wanted` 的 issue
- 在 issue 上评论表示您正在处理

### 2. 创建功能分支
```bash
git checkout -b feature/REQ-XXX-description
# 或修复错误:
git checkout -b fix/issue-description
```

### 3. 进行更改
- 遵循[编码规范](CODING_STANDARDS.md)
- 为新功能编写测试
- 根据需要更新文档
- 运行预提交钩子: `pre-commit run --all-files`

### 4. 测试更改
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_specific.py -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

### 5. 提交更改
```bash
git add .
git commit -m "REQ-XXX: 简要描述更改"
```

预提交钩子将自动运行并可能进行额外更改。

### 6. 推送并创建 Pull Request
```bash
git push origin feature/your-branch-name
```

然后在 GitHub 上创建 Pull Request，包含：
- 清晰的标题引用 issue
- 更改描述
- 截图/演示（如适用）
- 完成的测试

## 代码审查流程

### 贡献者
- 及时回复审查评论
- 将请求的更改作为单独提交或修改现有提交
- 保持 PR 专注于一个 issue/功能

### 审查者
- 检查代码风格和规范合规性
- 验证测试通过和覆盖率充足
- 手动测试功能（如需要）
- 建设性地提出改进建议

## 测试指南

### 单元测试
- 放置在 `tests/` 目录，镜像源码结构
- 文件命名: `test_*.py`
- 函数命名: `test_*`
- 使用描述性测试名称
- 测试成功和失败情况

### 集成测试
- 使用真实数据测试 API 端点
- 测试数据库操作
- 测试外部服务集成

### 测试覆盖率
- 目标 80%+ 代码覆盖率
- 重点关注关键业务逻辑
- 使用 `pytest-cov` 生成覆盖率报告

## 提交信息规范

遵循约定式提交格式：
```
type(scope): description

[optional body]

[optional footer]
```

类型:
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 代码风格更改（格式化等）
- `refactor`: 代码重构
- `test`: 测试添加/更改
- `chore`: 维护任务

示例:
```
feat(api): add user authentication endpoint
fix(routes): handle empty request body gracefully
docs(readme): update installation instructions
```

## 获取帮助

- 查看现有 [Issues](../../issues) 和文档
- 在 [Discussions](../../discussions) 中提问
- 加入社区聊天（如可用）

## 认可

贡献者将通过以下方式获得认可：
- GitHub 贡献者统计
- CHANGELOG.md 中的重大贡献
- 发布说明

感谢您帮助改进这个项目！🎉

### 2. Create a Feature Branch
```bash
git checkout -b feature/REQ-XXX-description
# or for bug fixes:
git checkout -b fix/issue-description
```

### 3. Make Changes
- Follow the [Coding Standards](CODING_STANDARDS.md)
- Write tests for new functionality
- Update documentation as needed
- Run pre-commit hooks: `pre-commit run --all-files`

### 4. Test Your Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run linting
flake8 app/ tests/

# Type checking
mypy app/
```

### 5. Commit Changes
```bash
git add .
git commit -m "REQ-XXX: Brief description of changes"
```

Pre-commit hooks will run automatically and may make additional changes.

### 6. Push and Create Pull Request
```bash
git push origin feature/your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title referencing the issue
- Description of changes made
- Screenshots/demo if applicable
- Testing done

## Code Review Process

### For Contributors
- Address review comments promptly
- Make requested changes as separate commits or amend existing ones
- Keep the PR focused on one issue/feature

### For Reviewers
- Check code style and standards compliance
- Verify tests pass and coverage is adequate
- Test the functionality manually if needed
- Suggest improvements constructively

## Testing Guidelines

### Unit Tests
- Place in `tests/` directory mirroring source structure
- Name files `test_*.py`
- Name functions `test_*`
- Use descriptive test names
- Test both success and failure cases

### Integration Tests
- Test API endpoints with realistic data
- Test database operations
- Test external service integrations

### Test Coverage
- Aim for 80%+ code coverage
- Focus on critical business logic
- Use `pytest-cov` for coverage reports

## Documentation

### Code Documentation
- Add docstrings to all public functions/classes
- Include parameter types and descriptions
- Document exceptions raised
- Update docstrings when changing functionality

### Project Documentation
- Update README.md for significant changes
- Add migration guides for breaking changes
- Update API documentation

## Issue Reporting

### Bug Reports
Please include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages/logs

### Feature Requests
Please include:
- Clear description of the feature
- Use case and benefits
- Mockups or examples if applicable

## Commit Message Guidelines

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(api): add user authentication endpoint
fix(routes): handle empty request body gracefully
docs(readme): update installation instructions
```

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

### Release Checklist
- [ ] All tests pass
- [ ] Code coverage meets requirements
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Pre-commit hooks pass
- [ ] CI/CD pipeline passes

## Getting Help

- Check existing [Issues](../../issues) and documentation
- Ask questions in [Discussions](../../discussions)
- Join our community chat (if available)

## Recognition

Contributors are recognized in:
- GitHub contributor statistics
- CHANGELOG.md for significant contributions
- Release notes

Thank you for contributing to make this project better!