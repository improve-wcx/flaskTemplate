# 依赖管理指南

本文档说明本项目的依赖管理方案和最佳实践。

## 🎯 设计原则

### 1. 分层管理 (Layered Management)
将依赖按功能和平台分层，避免混杂：

```
基础层 (base) → 测试层 (test) → 平台层 (platform) → 环境层 (env)
```

### 2. 平台分离 (Platform Separation)
不同操作系统的特定依赖分开管理：

- **Windows**: 使用 Waitress WSGI 服务器，需要 colorama
- **Linux**: 使用 Gunicorn WSGI 服务器
- **macOS**: 使用 Gunicorn WSGI 服务器

### 3. 环境区分 (Environment Distinction)
开发环境和生产环境依赖明确区分：

- **开发环境**: 包含测试工具、调试工具
- **生产环境**: 仅包含运行所需的最小依赖集

## 📁 文件结构

```
requirements/
├── base.txt          # 基础依赖（所有平台通用）
│   └── Flask, protobuf
├── test.txt          # 测试依赖（所有平台通用）
│   └── pytest, pytest-cov
├── dev.txt           # 开发工具（所有平台通用）
│   └── python-dotenv
├── linux.txt         # Linux 平台完整依赖
│   └── base + test + dev + gunicorn
├── windows.txt       # Windows 平台完整依赖
│   └── base + test + dev + waitress + colorama
├── prod.txt          # 生产环境依赖
└── dev.txt           # 开发环境依赖
```

## 🔧 依赖文件说明

### base.txt - 基础依赖
**用途**: 应用运行所需的核心依赖  
**包含**:
- Flask - Web 框架
- protobuf - 数据序列化

**适用场景**: 所有环境（开发、测试、生产）

### test.txt - 测试依赖
**用途**: 单元测试和覆盖率工具  
**包含**:
- pytest - 测试框架
- pytest-cov - 覆盖率报告

**适用场景**: 开发和 CI/CD 环境

### dev.txt - 开发工具
**用途**: 开发辅助工具  
**包含**:
- python-dotenv - 环境变量管理

**适用场景**: 开发环境

### linux.txt - Linux 平台
**用途**: Linux/Ubuntu 完整开发环境  
**包含**: base + test + dev + gunicorn

**安装命令**:
```bash
pip install -r requirements/linux.txt
```

### windows.txt - Windows 平台
**用途**: Windows 完整开发环境  
**包含**: base + test + dev + waitress + colorama

**安装命令**:
```bash
pip install -r requirements/windows.txt
```

### prod.txt - 生产环境
**用途**: 生产部署（最小依赖集）  
**包含**: base + 平台特定 WSGI 服务器

**注意**: 生产环境不应包含测试和开发工具

## 📋 版本控制策略

### 1. 版本范围约束
使用合理的版本范围，避免过严的限制：

```txt
# ✅ 推荐
Flask>=2.0,<3          # 接受 2.x 版本
pytest>=7.0,<9.0       # 接受 7.x-8.x 版本

# ❌ 不推荐
Flask==2.3.3           # 过于严格
pytest>=7.0            # 可能引入不兼容的大版本
```

### 2. 锁定生产版本
使用 `pip-tools` 锁定生产环境的精确版本：

```bash
# 安装 pip-tools
pip install pip-tools

# 生成锁定文件
pip-compile requirements/prod.in

# 安装锁定版本
pip-sync requirements/prod.txt
```

## 🔄 跨平台开发流程

### Windows 开发流程

```bash
# 1. 创建虚拟环境
py -m venv env
.\env\Scripts\Activate.ps1

# 2. 安装 Windows 依赖
pip install -r requirements\windows.txt

# 3. 生成 Protobuf 代码
python scripts\generate_protobuf_win.py

# 4. 运行测试
pytest tests/ -v

# 5. 开发
python run.py
```

### Linux 开发流程

```bash
# 1. 创建虚拟环境
python3 -m venv env
source env/bin/activate

# 2. 安装 Linux 依赖
pip install -r requirements/linux.txt

# 3. 生成 Protobuf 代码
python scripts/generate_protobuf.py

# 4. 运行测试
pytest tests/ -v

# 5. 开发
python run.py
```

### 自动检测平台

使用自动安装脚本：

```bash
python scripts/install_deps.py
```

脚本会自动：
1. 检测操作系统
2. 检测 Python 版本
3. 推荐正确的依赖文件
4. 安装依赖

## 🚀 生产部署

### Windows 生产部署

```bash
# 1. 安装生产依赖
pip install -r requirements\windows.txt

# 2. 使用 Waitress 运行
python wsgi.py
```

或使用 Waitress 直接运行：
```powershell
waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
```

### Linux 生产部署

```bash
# 1. 安装生产依赖
pip install -r requirements\linux.txt

# 2. 使用 Gunicorn 运行
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Docker 部署

```dockerfile
FROM python:3.9-slim

# 根据平台选择依赖文件
COPY requirements/linux.txt .
RUN pip install -r linux.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

## 🛠️ 维护指南

### 添加新依赖

1. **确定依赖类型**:
   - 核心功能 → `base.txt`
   - 测试工具 → `test.txt`
   - 开发工具 → `dev.txt`

2. **确定平台**:
   - 跨平台 → 添加到对应层
   - 平台特定 → 添加到平台文件

3. **指定版本范围**:
   ```txt
   # 使用语义化版本范围
   package>=1.0,<2.0
   ```

4. **更新文档**:
   - 在本文档说明新依赖的用途
   - 更新 README.md 的依赖说明

### 更新依赖版本

```bash
# 1. 检查可更新的包
pip list --outdated

# 2. 测试新版本
pip install package==new_version
pytest tests/ -v

# 3. 更新依赖文件
# 编辑对应的 .txt 文件

# 4. 提交更改
git add requirements/
git commit -m "chore: 更新 package 到新版本"
```

### 清理未使用依赖

```bash
# 安装 pip-autoremove
pip install pip-autoremove

# 查看依赖树
pip freeze

# 移除未使用的包
pip-autoremove package-name -y
```

## 📊 依赖关系图

```
┌─────────────────────────────────────────────────┐
│              开发环境 (dev)                      │
├─────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ base.txt │─▶│ test.txt │─▶│ dev.txt  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│       │              │              │           │
│       └──────────────┴──────────────┘           │
│                    │                            │
│       ┌────────────┴────────────┐              │
│       ▼                         ▼              │
│  ┌──────────┐            ┌──────────┐          │
│  │linux.txt │            │windows.txt│         │
│  │ +gunicorn│            │+waitress  │         │
│  └──────────┘            └──────────┘          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│             生产环境 (prod)                      │
├─────────────────────────────────────────────────┤
│  ┌──────────┐                                   │
│  │ base.txt │                                   │
│  └──────────┘                                   │
│       │                                         │
│       ▼                                         │
│  ┌──────────┐            ┌──────────┐          │
│  │linux.txt │            │windows.txt│          │
│  │ +gunicorn│            │+waitress  │          │
│  └──────────┘            └──────────┘          │
└─────────────────────────────────────────────────┘
```

## 🔍 常见问题

### Q: 为什么要分层管理依赖？

A: 
1. **清晰性**: 每个文件职责明确，易于维护
2. **灵活性**: 可以按需安装不同层次的依赖
3. **可复用**: 基础依赖可以被多个平台文件复用
4. **可测试**: 测试依赖可以独立更新

### Q: 如何确定某个依赖应该放在哪个文件？

A: 使用以下决策树：

```
是核心运行依赖吗？
├─ 是 → base.txt
└─ 否 → 是测试工具吗？
        ├─ 是 → test.txt
        └─ 否 → 是平台特定的吗？
                ├─ 是 → linux.txt / windows.txt
                └─ 否 → dev.txt
```

### Q: 如何在 CI/CD 中使用？

A: 在 CI/CD 配置中使用对应的平台文件：

```yaml
# GitHub Actions 示例
- name: Install dependencies
  run: |
    pip install -r requirements/linux.txt
    
- name: Run tests
  run: pytest tests/ -v
```

### Q: 如何管理不同 Python 版本的兼容性？

A: 
1. 在 `setup.py` 或 `pyproject.toml` 中指定 Python 版本要求
2. 使用 `tox` 或 `nox` 在多版本上测试
3. 在 CI/CD 中配置多版本测试矩阵

## 📚 参考资料

- [pip 官方文档](https://pip.pypa.io/)
- [Python 依赖管理最佳实践](https://packaging.python.org/)
- [Flask 官方文档 - 部署](https://flask.palletsprojects.com/deploying/)
- [pip-tools](https://github.com/jazzband/pip-tools)
- [Poetry](https://python-poetry.org/) - 现代化的 Python 包管理工具

## 📝 更新历史

- 2026-03-16: 初始版本，采用分层依赖管理方案
- 2026-03-16: 添加跨平台支持说明
