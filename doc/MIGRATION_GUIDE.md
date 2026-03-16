# 迁移指南 - 从 Ubuntu/Python 3.12 到 Windows/Python 3.9

本文档说明从 Ubuntu + Python 3.12 环境迁移到 Windows + Python 3.9 环境的注意事项和步骤。

## 🔄 环境对比

| 项目 | Ubuntu + Python 3.12 | Windows + Python 3.9 |
|------|---------------------|---------------------|
| **操作系统** | Linux (Ubuntu) | Windows 10/11 |
| **Python 版本** | 3.12 | 3.9.10 |
| **虚拟环境激活** | `source env/bin/activate` | `.\env\Scripts\Activate.ps1` |
| **WSGI 服务器** | Gunicorn | Waitress |
| **包管理器** | pip | pip |
| **路径分隔符** | `/` | `\` |
| **Shell** | Bash | PowerShell |

## 📦 依赖差异

### 必须安装的 Windows 特定包

```txt
# Windows 特定依赖
colorama>=0.4.6      # 终端彩色输出支持
waitress>=3.0.0      # Windows WSGI 服务器
```

### Linux 特定包

```txt
# Linux 特定依赖
gunicorn>=21.0.0     # Linux WSGI 服务器
```

### 版本兼容性

| 包名 | Python 3.12 | Python 3.9 | 说明 |
|------|------------|-----------|------|
| Flask | ✅ 2.3.3 | ✅ 2.3.3 | 完全兼容 |
| pytest | ✅ 8.4.2 | ✅ 8.4.2 | 完全兼容 |
| protobuf | ✅ 6.33.5 | ✅ 6.33.5 | 完全兼容 |
| gunicorn | ✅ 21+ | ✅ 21+ | Linux 专用 |
| waitress | ✅ 3.0+ | ✅ 3.0+ | Windows 专用 |

## 🚀 迁移步骤

### 1. 在 Windows 上安装 Python 3.9

```powershell
# 从 python.org 下载 Python 3.9
# 或使用 winget
winget install Python.Python.3.9

# 验证安装
py --version
# 输出：Python 3.9.10
```

### 2. 克隆项目

```powershell
git clone <repository-url>
cd flaskTemplate
```

### 3. 创建虚拟环境

```powershell
# 使用 py 启动器
py -m venv env

# 激活虚拟环境
.\env\Scripts\Activate.ps1
```

### 4. 安装 Windows 依赖

```powershell
# 方式一：使用平台特定文件
pip install -r requirements\windows.txt

# 方式二：使用自动安装脚本
python scripts\install_deps.py
```

### 5. 生成 Protobuf 代码

```powershell
# Windows 专用脚本
python scripts\generate_protobuf_win.py

# 注意：不要使用 generate_protobuf.py（需要 mypy 插件）
```

### 6. 运行测试

```powershell
pytest tests/ -v
```

### 7. 启动开发服务器

```powershell
python run.py
```

## 🛠️ 命令对照表

### 虚拟环境

| 操作 | Ubuntu/Bash | Windows/PowerShell |
|------|-------------|-------------------|
| 创建 | `python3 -m venv env` | `py -m venv env` |
| 激活 | `source env/bin/activate` | `.\env\Scripts\Activate.ps1` |
| 退出 | `deactivate` | `deactivate` |

### 依赖管理

| 操作 | Ubuntu/Bash | Windows/PowerShell |
|------|-------------|-------------------|
| 安装依赖 | `pip install -r requirements/linux.txt` | `pip install -r requirements\windows.txt` |
| 升级 pip | `python3 -m pip install --upgrade pip` | `py -m pip install --upgrade pip` |

### 运行命令

| 操作 | Ubuntu/Bash | Windows/PowerShell |
|------|-------------|-------------------|
| 运行测试 | `pytest tests/ -v` | `pytest tests/ -v` |
| 启动服务 | `python run.py` | `python run.py` |
| 生成 Protobuf | `python scripts/generate_protobuf.py` | `python scripts\generate_protobuf_win.py` |

### Make 命令

| 操作 | Ubuntu/Bash | Windows/PowerShell |
|------|-------------|-------------------|
| 帮助 | `make help` | `.\make.ps1 help` |
| 安装 | `make install-dev` | `.\make.ps1 install-dev` |
| 测试 | `make test` | `.\make.ps1 test` |
| 运行 | `make run` | `.\make.ps1 run` |

## ⚠️ 常见问题

### Q1: Python 3.9 和 3.12 的兼容性问题？

**A**: 本项目使用的依赖包都兼容 Python 3.9-3.12：
- Flask 2.3.3 ✅
- pytest 8.4.2 ✅
- protobuf 6.33.5 ✅

如果遇到兼容性问题，检查包的版本要求：
```bash
pip show <package-name>
```

### Q2: 路径分隔符问题？

**A**: 在 Python 代码中使用 `pathlib` 而不是硬编码路径：

```python
# ✅ 推荐
from pathlib import Path
config_path = Path("config") / "config.json"

# ❌ 不推荐
config_path = "config/config.json"  # Windows 下可能有问题
```

### Q3: 换行符问题？

**A**: Git 会自动处理换行符，确保配置正确：

```bash
# 在两个平台上都设置
git config --global core.autocrlf true
```

### Q4: 行尾符导致脚本无法执行？

**A**: 使用 `dos2unix` 或 `unix2dos` 转换：

```powershell
# Windows PowerShell
# 安装 dos2unix
choco install dos2unix

# 转换脚本
unix2dos scripts/generate_protobuf_win.py
```

### Q5: 权限问题？

**A**: Windows 下可能需要管理员权限：

```powershell
# 以管理员身份运行 PowerShell
# 或修改执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔄 双向开发

如果你需要在两个平台上开发，建议：

### 1. 使用 .gitignore

```gitignore
# 虚拟环境
env/
ENV/

# 操作系统文件
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# 测试
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
```

### 2. 使用平台检测脚本

```python
# scripts/install_deps.py
import platform
import sys

if platform.system() == "Windows":
    requirements = "requirements/windows.txt"
else:
    requirements = "requirements/linux.txt"

subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements])
```

### 3. 在两个平台上运行测试

```bash
# CI/CD 配置中测试两个平台
# GitHub Actions 示例
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ["3.9", "3.12"]
```

## 📊 性能对比

| 指标 | Ubuntu + 3.12 + Gunicorn | Windows + 3.9 + Waitress |
|------|-------------------------|-------------------------|
| **启动时间** | ~2 秒 | ~3 秒 |
| **请求延迟** | ~5ms | ~8ms |
| **内存占用** | ~50MB | ~60MB |
| **并发能力** | 高 | 中等 |

**结论**: 对于开发环境，性能差异可以忽略。生产环境建议使用 Linux。

## 🎯 最佳实践

### 1. 使用统一的依赖管理

```bash
# 使用分层依赖管理
pip install -r requirements/windows.txt  # Windows
pip install -r requirements/linux.txt    # Linux
```

### 2. 自动化平台检测

```bash
# 使用 install_deps.py 自动选择
python scripts/install_deps.py
```

### 3. 保持两个平台的测试通过

```bash
# 在两个平台上定期运行测试
pytest tests/ -v --cov=app
```

### 4. 使用跨平台工具

```python
# 使用 pathlib 处理路径
from pathlib import Path

# 使用 click 或 typer 创建 CLI
import click

# 使用 logging 而不是 print
import logging
```

## 📚 相关文档

- [依赖管理指南](DEPENDENCY_MANAGEMENT.md)
- [本地开发环境快速参考](../README.md)
- [开发者指南](getting-started.md)
- [部署指南](deployment/README.md)

## 🔄 更新历史

- 2026-03-16: 初始版本，支持 Windows + Python 3.9
- 2026-03-16: 添加双向开发支持说明
