# 依赖管理迁移说明

## 📋 变更概述

**日期**: 2026-03-16  
**版本**: v2.0.0  
**变更类型**: 依赖管理结构重构

## 🔄 主要变更

### 1. 依赖文件结构调整

#### 变更前
```
requirements.txt          # 所有依赖混在一起
requirements-dev.txt      # 开发依赖
```

#### 变更后
```
requirements/
├── base.txt          # 基础依赖（Flask, protobuf）
├── test.txt          # 测试依赖（pytest, pytest-cov）
├── dev.txt           # 开发工具（python-dotenv）
├── windows.txt       # Windows 平台完整依赖
├── linux.txt         # Linux 平台完整依赖
└── prod.txt          # 生产环境依赖
```

### 2. 删除的文件

- ❌ `requirements.txt` (根目录)
- ❌ `requirements-dev.txt` (根目录)

### 3. 新增的文件

- ✅ `requirements/base.txt`
- ✅ `requirements/test.txt`
- ✅ `requirements/dev.txt`
- ✅ `requirements/windows.txt`
- ✅ `requirements/linux.txt`
- ✅ `requirements/prod.txt`
- ✅ `scripts/install_deps.py` (自动平台检测)
- ✅ `scripts/generate_protobuf_win.py` (Windows 专用)
- ✅ `make.ps1` (Windows PowerShell Makefile)
- ✅ `doc/DEPENDENCY_MANAGEMENT.md`
- ✅ `doc/MIGRATION_GUIDE.md`
- ✅ `doc/QUICK_REFERENCE.md`
- ✅ `doc/DEPENDENCY_STRATEGY.md`

## 📝 迁移指南

### 对于开发者

#### 1. 拉取最新代码
```bash
git pull origin main
```

#### 2. 删除旧的虚拟环境（可选）
```bash
# Linux/macOS
deactivate
rm -rf env

# Windows
deactivate
Remove-Item -Recurse -Force env
```

#### 3. 创建新的虚拟环境
```bash
# Linux/macOS
python3 -m venv env
source env/bin/activate

# Windows
py -m venv env
.\env\Scripts\Activate.ps1
```

#### 4. 安装新依赖

**方式一：自动检测（推荐）**
```bash
python scripts/install_deps.py
```

**方式二：手动选择平台**
```bash
# Linux/macOS
pip install -r requirements/linux.txt

# Windows
pip install -r requirements/windows.txt
```

#### 5. 生成 Protobuf 代码
```bash
# Linux/macOS
python scripts/generate_protobuf.py

# Windows
python scripts\generate_protobuf_win.py
```

#### 6. 运行测试验证
```bash
pytest tests/ -v
```

### 对于 CI/CD

更新 CI/CD 配置文件中的依赖安装命令：

#### GitHub Actions 示例
```yaml
# 变更前
- run: pip install -r requirements-dev.txt

# 变更后
- run: pip install -r requirements/linux.txt
```

#### GitLab CI 示例
```yaml
# 变更前
before_script:
  - pip install -r requirements-dev.txt

# 变更后
before_script:
  - pip install -r requirements/linux.txt
```

## 📚 文档更新

### 已更新的文档

1. **README.md** - 主文档，整合了所有快速开始说明
2. **doc/getting-started.md** - 开发者入门指南
3. **doc/deployment/README.md** - 部署指南（包含 Docker）
4. **doc/protobuf/README.md** - Protobuf 使用指南
5. **doc/DEPENDENCY_MANAGEMENT.md** - 依赖管理详解（新增）
6. **doc/MIGRATION_GUIDE.md** - 跨平台迁移指南（新增）
7. **doc/QUICK_REFERENCE.md** - 快速参考（新增）
8. **doc/DEPENDENCY_STRATEGY.md** - 依赖策略说明（新增）

### 废弃的文档

- ❌ `LOCAL_SETUP.md` (内容已整合到 README.md)

## 🎯 使用新命令

### 依赖安装

```bash
# 自动检测平台并安装
python scripts/install_deps.py

# 或手动选择
pip install -r requirements/windows.txt  # Windows
pip install -r requirements/linux.txt    # Linux
```

### 运行命令

```bash
# Windows
.\make.ps1 test
.\make.ps1 run
.\make.ps1 protobuf

# Linux/macOS
make test
make run
make protobuf
```

## ⚠️ 注意事项

### 1. Python 版本兼容性

新结构支持 Python 3.9-3.12：
- Flask 2.3.3 ✅
- pytest 8.4.2 ✅
- protobuf 6.33.5 ✅

### 2. 平台特定依赖

- **Windows**: 自动安装 `waitress` 和 `colorama`
- **Linux**: 自动安装 `gunicorn`

### 3. 路径分隔符

在文档和脚本中：
- Windows 使用 `\`
- Linux/macOS 使用 `/`

### 4. 虚拟环境激活

```bash
# Linux/macOS
source env/bin/activate

# Windows
.\env\Scripts\Activate.ps1
```

## 🐛 故障排除

### 问题 1: 找不到 requirements.txt

**原因**: 文件已移动到 `requirements/` 目录

**解决**:
```bash
# 使用新的路径
pip install -r requirements/linux.txt
# 或
pip install -r requirements/windows.txt
```

### 问题 2: 依赖安装失败

**解决**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements/<platform>.txt
```

### 问题 3: Protobuf 生成失败

**Windows**:
```bash
python scripts\generate_protobuf_win.py
```

**Linux**:
```bash
# 确保安装 protoc
sudo apt-get install protobuf-compiler
python scripts/generate_protobuf.py
```

## 📊 变更统计

| 类型 | 数量 |
|------|------|
| 新增文件 | 13 |
| 删除文件 | 3 |
| 更新文件 | 8 |
| 总变更 | 24 |

## 🤝 贡献

如果你在使用过程中遇到问题，请：
1. 查看 [DEPENDENCY_MANAGEMENT.md](doc/DEPENDENCY_MANAGEMENT.md)
2. 查看 [MIGRATION_GUIDE.md](doc/MIGRATION_GUIDE.md)
3. 提交 Issue 或 Pull Request

## 📅 版本历史

- **v2.0.0** (2026-03-16): 重构依赖管理，支持跨平台
- **v1.0.0**: 初始版本

---

**迁移完成日期**: 2026-03-16  
**维护者**: 开发团队  
**联系方式**: 提交 Issue 或 Pull Request
