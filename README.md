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
- **结构化日志** - JSON 格式日志输出
- **完整测试** - 19+ 单元测试覆盖
- **应用工厂** - 灵活的应用创建模式

## 文档

详细文档请查看 [doc/](doc/) 目录：

- [部署指南](doc/deployment/README.md) - 运行和部署说明
- [路由开发](doc/routes/development.md) - 如何添加路由
- [API 设计](doc/api/README.md) - API 设计规范
- [测试指南](doc/testing/README.md) - 编写单元测试
- [项目架构](doc/deployment/architecture.md) - 架构说明

## 技术栈

- Flask 2.3.3
- Python 3.12
- pytest 9.0
- Gunicorn
