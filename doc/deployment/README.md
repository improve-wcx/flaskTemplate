# 部署指南

> 包含开发环境设置、生产环境部署、Protobuf 编译等完整说明。

## 📋 目录

- [环境要求](#环境要求)
- [开发环境设置](#开发环境设置)
- [生产环境部署](#生产环境部署)
- [Protobuf 编译](#protobuf-编译)
- [配置说明](#配置说明)
- [监控和日志](#监控和日志)
- [故障排查](#故障排查)

---

## 环境要求

### 必需

- **Python**: 3.12+
- **pip**: 最新版
- **Git**: 用于代码管理

### 可选

- **Protocol Buffers 编译器**: 仅当使用 protobuf 时
  - Ubuntu/Debian: `sudo apt-get install protobuf-compiler`
  - macOS: `brew install protobuf`
  - Windows: 从 [GitHub Releases](https://github.com/protocolbuffers/protobuf/releases) 下载

- **生产环境服务器**
  - Gunicorn (Linux/Mac)
  - Waitress (Windows)
  - Nginx (反向代理)

---

## 开发环境设置

### 1. 克隆项目

```bash
git clone <repository-url>
cd projectTemplate
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv env

# 激活虚拟环境
source env/bin/activate  # Linux/Mac
# 或 env\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
# Linux/macOS - 安装开发依赖
pip install -r requirements/linux.txt

# Windows - 安装开发依赖
# pip install -r requirements/windows.txt

# 或仅安装运行依赖（生产环境）
# Linux:
# pip install -r requirements/base.txt && pip install gunicorn

# Windows:
# pip install -r requirements/base.txt && pip install waitress
```

### 4. 编译 Protobuf（如使用）

```bash
# 使用项目脚本（推荐）
python scripts/generate_protobuf.py

# 或手动编译
protoc --python_out=app/proto --pyi_out=app/proto proto/*.proto
```

### 5. 运行应用

```bash
# 开发模式（自动重载）
python run.py

# 访问 http://127.0.0.1:5000
```

### 6. 运行测试

```bash
pytest tests/ -v
```

---

## 生产环境部署

### 方案一：Gunicorn（推荐）

#### 1. 安装 Gunicorn

```bash
pip install gunicorn
```

#### 2. 启动服务

```bash
# 基本启动
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# 生产配置
gunicorn \
  --workers 4 \
  --worker-class gthread \
  --threads 2 \
  --bind 0.0.0.0:5000 \
  --timeout 30 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  wsgi:app
```

#### 3. 使用 systemd（Linux）

创建 `/etc/systemd/system/projectTemplate.service`:

```ini
[Unit]
Description=ProjectTemplate Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/projectTemplate
Environment="PATH=/var/www/projectTemplate/env/bin"
ExecStart=/var/www/projectTemplate/env/bin/gunicorn \
  --workers 4 \
  --bind 127.0.0.1:5000 \
  wsgi:app

Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start projectTemplate
sudo systemctl enable projectTemplate
sudo systemctl status projectTemplate
```

#### 4. Nginx 配置（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 方案二：Docker 部署

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 根据平台选择依赖文件
# Linux 部署
COPY requirements/linux.txt .
RUN pip install --no-cache-dir -r linux.txt

# Windows 部署（使用基础镜像）
# COPY requirements/base.txt .
# RUN pip install --no-cache-dir -r base.txt
# RUN pip install waitress

# 复制代码
COPY . .

# 编译 protobuf
RUN python scripts/generate_protobuf.py

# 暴露端口
EXPOSE 5000

# 启动
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

#### 2. 构建和运行

```bash
# 构建镜像
docker build -t projectTemplate .

# 运行容器
docker run -d -p 5000:5000 --name app projectTemplate

# 查看日志
docker logs -f app
```

---

## Protobuf 编译

### 何时需要编译

- 添加新的 `.proto` 文件
- 修改现有的 `.proto` 文件
- 切换分支后（如果 proto 文件有变化）

### 编译步骤

#### 方法一：使用项目脚本（推荐）

```bash
python scripts/generate_protobuf.py
```

该脚本会自动：
- 查找所有 `.proto` 文件
- 生成 `.pb2.py` 和 `.pb2.pyi` 文件
- 输出到 `app/proto/` 目录

#### 方法二：手动编译

```bash
# 编译单个文件
protoc --python_out=app/proto --pyi_out=app/proto proto/demo.proto

# 编译所有文件
protoc --python_out=app/proto --pyi_out=app/proto proto/*.proto
```

### 验证编译

```bash
# 检查生成的文件
ls -la app/proto/*_pb2.py

# 测试导入
python -c "from app.proto import demo_pb2; print('OK')"
```

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_ENV` | 运行环境 | `development` |
| `FLASK_DEBUG` | 调试模式 | `1` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### 配置文件

项目使用 `config/config.json` 管理配置：

```json
{
  "development": {
    "app": {
      "host": "127.0.0.1",
      "port": 5000,
      "debug": true
    },
    "logging": {
      "level": "DEBUG",
      "format": "json"
    }
  },
  "production": {
    "app": {
      "host": "0.0.0.0",
      "port": 5000,
      "debug": false
    },
    "logging": {
      "level": "WARNING",
      "format": "json"
    }
  }
}
```

### 切换环境

```bash
# 开发环境
export FLASK_ENV=development
python run.py

# 生产环境
export FLASK_ENV=production
python run.py
```

---

## 监控和日志

### 日志位置

```
logs/
├── app.log          # 应用日志
├── access.log       # 访问日志（生产环境）
└── error.log        # 错误日志（生产环境）
```

### 查看日志

```bash
# 实时查看
tail -f logs/app.log

# 查看最近 100 行
tail -n 100 logs/app.log

# 搜索特定请求
grep "request-id-xxx" logs/app.log

# 搜索错误
grep "ERROR" logs/app.log
```

### 日志格式

应用使用 JSON 格式日志，包含以下字段：

```json
{
  "timestamp": "2026-03-16T10:00:00",
  "level": "INFO",
  "pid": 12345,
  "tid": 140123456,
  "logger": "projectTemplate",
  "message": "GET /api/health",
  "pathname": "/app/__init__.py",
  "lineno": 95,
  "request_id": "uuid-xxx"
}
```

---

## 故障排查

### 问题：端口被占用

```bash
# 查找占用端口的进程
lsof -ti:5000

# 杀死进程
kill -9 <PID>

# 或修改端口
export FLASK_PORT=5001
python run.py
```

### 问题：Protobuf 导入错误

```bash
# 重新编译
python scripts/generate_protobuf.py

# 检查生成的文件
ls app/proto/*_pb2.py

# 验证导入
python -c "from app.proto import demo_pb2"
```

### 问题：依赖冲突

```bash
# 重新创建虚拟环境
deactivate
rm -rf env

# Linux/macOS
python3 -m venv env
source env/bin/activate
pip install -r requirements/linux.txt

# Windows
# py -m venv env
# .\env\Scripts\Activate.ps1
# pip install -r requirements/windows.txt
```

### 问题：测试失败

```bash
# 查看详细错误
pytest tests/ -v --tb=long

# 只运行失败的测试
pytest tests/ -v --lf

# 清除缓存重新运行
pytest tests/ -v --cache-clear
```

---

## 性能优化

### 1. 使用 Gunicorn

```bash
# 根据 CPU 核心数设置 worker 数
workers = (2 * CPU_cores) + 1

# 示例：4 核 CPU
gunicorn -w 9 -b 0.0.0.0:5000 wsgi:app
```

### 2. 启用缓存

（如使用缓存，在此说明）

### 3. 数据库连接池

（如使用数据库，在此说明）

### 4. 静态文件服务

生产环境使用 Nginx 服务静态文件：

```nginx
location /static/ {
    alias /var/www/projectTemplate/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 安全建议

1. **不要提交敏感信息**
   - 将 `.env` 添加到 `.gitignore`
   - 使用环境变量管理密钥

2. **启用 HTTPS**
   - 使用 Let's Encrypt 免费证书
   - Nginx 配置 SSL

3. **限制访问**
   - 使用防火墙限制 IP
   - 配置 CORS 策略

4. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

---

## 相关文档

- [开发者指南](../getting-started.md)
- [CLI 使用指南](../cli/README.md)
- [日志系统说明](../log/README.md)
- [Protobuf 使用指南](../protobuf/README.md)
