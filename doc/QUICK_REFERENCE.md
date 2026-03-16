# 快速参考 - 跨平台开发命令

## 🪟 Windows 命令

### 虚拟环境
```powershell
# 创建
py -m venv env

# 激活
.\env\Scripts\Activate.ps1

# 退出
deactivate
```

### 依赖安装
```powershell
# 自动检测平台
python scripts\install_deps.py

# 手动安装 Windows 依赖
pip install -r requirements\windows.txt

# 仅安装基础依赖
pip install -r requirements\base.txt
```

### 开发命令
```powershell
# 生成 Protobuf 代码
python scripts\generate_protobuf_win.py

# 运行测试
pytest tests/ -v

# 启动开发服务器
python run.py

# 使用 Make 脚本
.\make.ps1 test
.\make.ps1 run
.\make.ps1 protobuf
```

### 生产部署
```powershell
# 使用 Waitress
python wsgi.py

# 或直接运行
waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
```

---

## 🐧 Linux/Ubuntu 命令

### 虚拟环境
```bash
# 创建
python3 -m venv env

# 激活
source env/bin/activate

# 退出
deactivate
```

### 依赖安装
```bash
# 自动检测平台
python scripts/install_deps.py

# 手动安装 Linux 依赖
pip install -r requirements/linux.txt

# 仅安装基础依赖
pip install -r requirements/base.txt
```

### 开发命令
```bash
# 生成 Protobuf 代码
python scripts/generate_protobuf.py

# 运行测试
pytest tests/ -v

# 启动开发服务器
python run.py

# 使用 Make
make test
make run
make protobuf
```

### 生产部署
```bash
# 使用 Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## 📦 依赖文件说明

| 文件 | 用途 | 适用平台 |
|------|------|---------|
| `base.txt` | 核心依赖 (Flask, protobuf) | 所有平台 |
| `test.txt` | 测试工具 (pytest, pytest-cov) | 所有平台 |
| `dev.txt` | 开发工具 (python-dotenv) | 所有平台 |
| `windows.txt` | Windows 完整依赖 | Windows |
| `linux.txt` | Linux 完整依赖 | Linux |
| `prod.txt` | 生产环境依赖 | 所有平台 |

---

## 🔍 快速诊断

### 问题：虚拟环境无法激活
**Windows**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题：Protobuf 生成失败
**Windows**: 使用 `generate_protobuf_win.py`  
**Linux**: 确保安装 `protoc` 和 `grpcio-tools`

### 问题：端口 5000 被占用
修改 `config/config.json` 中的 `port` 配置

### 问题：依赖安装失败
```bash
# 升级 pip
python -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements/<platform>.txt
```

---

## 🌐 访问应用

- **开发服务器**: http://127.0.0.1:5000
- **健康检查**: http://127.0.0.1:5000/api/health
- **API 列表**: http://127.0.0.1:5000/api/apis

---

## 📚 更多文档

- [完整 README](../README.md)
- [依赖管理指南](DEPENDENCY_MANAGEMENT.md)
- [迁移指南](MIGRATION_GUIDE.md)
- [开发者指南](getting-started.md)
