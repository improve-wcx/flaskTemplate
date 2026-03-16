# 跨平台依赖管理方案总结

## 📋 背景

原项目存在以下问题：
1. **平台依赖混杂**：Windows 和 Linux 的依赖混在同一个文件
2. **Python 版本不统一**：Ubuntu 使用 Python 3.12，Windows 使用 Python 3.9
3. **文档分散**：本地设置说明在多个文件中重复
4. **缺乏最佳实践**：没有遵循业界标准的依赖管理方案

## 🎯 业界最佳实践方案对比

### 方案 1: 分层依赖管理（本项目采用）⭐

**优点**:
- ✅ 简单直观，易于理解
- ✅ 兼容性好，支持所有 Python 版本
- ✅ 灵活性高，可以按需安装
- ✅ 维护成本低
- ✅ 被 Flask/Django 等主流框架采用

**缺点**:
- ⚠️ 需要手动维护多个文件
- ⚠️ 版本锁定需要额外工具（如 pip-tools）

**适用场景**: 中小型 Web 项目、微服务

**文件结构**:
```
requirements/
├── base.txt          # 基础依赖
├── test.txt          # 测试依赖
├── dev.txt           # 开发工具
├── windows.txt       # Windows 平台
├── linux.txt         # Linux 平台
└── prod.txt          # 生产环境
```

### 方案 2: pip-tools

**优点**:
- ✅ 自动解析依赖
- ✅ 精确版本锁定
- ✅ 支持分层管理
- ✅ 生产环境推荐

**缺点**:
- ⚠️ 需要学习额外工具
- ⚠️ 构建流程变复杂

**适用场景**: 生产环境、需要精确版本控制的项目

**工作流程**:
```bash
# 定义依赖
echo "Flask>=2.0" > requirements/base.in

# 生成锁定文件
pip-compile requirements/base.in

# 安装锁定版本
pip-sync requirements/base.txt
```

### 方案 3: Poetry

**优点**:
- ✅ 现代化，一体化解决方案
- ✅ 自动依赖解析
- ✅ 内置虚拟环境管理
- ✅ 支持发布到 PyPI
- ✅ 跨平台支持最好

**缺点**:
- ⚠️ 学习曲线较陡
- ⚠️ 需要安装额外工具
- ⚠️ 与 pip 生态不完全兼容

**适用场景**: 新项目、Python 库/包开发

**示例**:
```toml
# pyproject.toml
[tool.poetry]
name = "flask-template"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
Flask = "^2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
```

### 方案 4: setup.py extras_require

**优点**:
- ✅ Python 标准方式
- ✅ 适合库/包开发
- ✅ 可以发布到 PyPI

**缺点**:
- ⚠️ 不适合应用开发
- ⚠️ 配置复杂
- ⚠️ 不够灵活

**适用场景**: Python 库、SDK 开发

**示例**:
```python
# setup.py
setup(
    name="flask-template",
    extras_require={
        "dev": ["pytest", "black"],
        "prod": ["gunicorn", "waitress"],
    },
)
```

## 🏆 本项目选择：分层依赖管理

### 选择理由

1. **项目类型**: Flask Web 应用，不是 Python 库
2. **团队规模**: 中小型团队，需要简单方案
3. **学习成本**: 团队成员熟悉 pip
4. **灵活性**: 支持多平台、多环境
5. **维护性**: 易于理解和维护

### 实现方案

#### 1. 分层结构

```
requirements/
├── base.txt          # 核心依赖（Flask, protobuf）
├── test.txt          # 测试依赖（pytest, pytest-cov）
├── dev.txt           # 开发工具（python-dotenv）
├── windows.txt       # Windows 完整依赖
│   └── base + test + dev + waitress + colorama
├── linux.txt         # Linux 完整依赖
│   └── base + test + dev + gunicorn
└── prod.txt          # 生产环境依赖
```

#### 2. 平台检测

```python
# scripts/install_deps.py
import platform

def get_platform():
    system = platform.system().lower()
    if system == 'linux':
        return 'linux'
    elif system == 'windows':
        return 'windows'
    return 'unknown'
```

#### 3. 自动化脚本

- `install_deps.py` - 自动检测平台并安装
- `generate_protobuf_win.py` - Windows 专用 Protobuf 生成
- `make.ps1` - Windows PowerShell Makefile

#### 4. 文档整合

- **README.md** - 主文档，包含快速开始
- **doc/DEPENDENCY_MANAGEMENT.md** - 依赖管理详解
- **doc/MIGRATION_GUIDE.md** - 跨平台迁移指南
- **doc/QUICK_REFERENCE.md** - 快速参考

## 📊 方案对比表

| 特性 | 分层管理 | pip-tools | Poetry | setup.py |
|------|---------|-----------|--------|----------|
| **学习曲线** | ⭐ 简单 | ⭐⭐ 中等 | ⭐⭐⭐ 较陡 | ⭐⭐ 中等 |
| **灵活性** | ⭐⭐⭐ 高 | ⭐⭐ 中等 | ⭐⭐⭐ 高 | ⭐ 低 |
| **跨平台** | ⭐⭐⭐ 好 | ⭐⭐⭐ 好 | ⭐⭐⭐ 最好 | ⭐⭐ 一般 |
| **版本锁定** | ⭐⭐ 手动 | ⭐⭐⭐ 自动 | ⭐⭐⭐ 自动 | ⭐ 无 |
| **适用场景** | Web 应用 | 生产环境 | 新项目/库 | Python 库 |
| **维护成本** | ⭐⭐ 低 | ⭐⭐ 低 | ⭐⭐⭐ 中 | ⭐⭐ 中 |

## 🚀 实施效果

### 改进前

```
❌ 依赖混杂
requirements.txt:
  Flask
  pytest
  gunicorn  # Linux 专用
  waitress  # Windows 专用

❌ 文档分散
- README.md 有部分内容
- LOCAL_SETUP.md 重复内容
- 没有统一的依赖管理说明
```

### 改进后

```
✅ 分层清晰
requirements/
  ├── base.txt       # 核心依赖
  ├── test.txt       # 测试依赖
  ├── windows.txt    # Windows 专用
  └── linux.txt      # Linux 专用

✅ 文档统一
- README.md 整合所有快速开始
- DEPENDENCY_MANAGEMENT.md 详细说明
- MIGRATION_GUIDE.md 跨平台支持
- QUICK_REFERENCE.md 快速查询
```

## 📈 业界趋势

### 1. 分层依赖管理（当前主流）

被以下项目采用：
- Flask 官方示例
- Django 项目模板
- FastAPI 示例项目
- 大多数中小型 Web 应用

### 2. Poetry 崛起（未来趋势）

越来越多的新项目采用：
- 现代化 Python 项目
- Python 库/包开发
- 需要发布到 PyPI 的项目

### 3. pip-tools（生产环境）

适合：
- 需要精确版本锁定的生产环境
- 企业级应用
- 合规性要求高的项目

## 💡 建议

### 对于本项目

1. **当前**: 继续使用分层依赖管理
2. **短期**: 添加 pip-tools 用于生产环境版本锁定
3. **长期**: 考虑迁移到 Poetry（如果需要发布为库）

### 对于新项目

- **Web 应用**: 分层依赖管理
- **Python 库**: Poetry
- **企业应用**: 分层管理 + pip-tools

### 对于团队

- **小团队**: 分层管理（简单）
- **大团队**: Poetry（标准化）
- **多项目**: 统一使用一种方案

## 📚 参考资料

### 官方文档

- [pip 官方文档](https://pip.pypa.io/)
- [Python 打包指南](https://packaging.python.org/)
- [Flask 部署](https://flask.palletsprojects.com/deploying/)

### 最佳实践

- [12-Factor App](https://12factor.net/)
- [Python 依赖管理最佳实践](https://hynek.me/articles/python-dependencies/)
- [The Hitchhiker's Guide to Packaging](https://the-hitchhikers-guide-to-packaging.readthedocs.io/)

### 工具文档

- [pip-tools](https://github.com/jazzband/pip-tools)
- [Poetry](https://python-poetry.org/docs/)
- [tox](https://tox.wiki/) - 多环境测试

## 🔄 更新历史

- 2026-03-16: 初始版本，采用分层依赖管理
- 2026-03-16: 添加跨平台支持
- 2026-03-16: 整合文档，消除重复内容
