# 部署指南

## 快速开始

### 1. 环境要求

- Python 3.12+
- pip 或 poetry
- (可选) Gunicorn/uWSGI (生产环境)

### 2. 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd projectTemplate

# 创建虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac
# 或 env\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements-dev.txt
```

### 3. 配置环境

```bash
# 复制环境变量示例
cp .env.example .env

# 编辑 .env 文件
# FLASK_ENV=development  # development, testing, production
```

### 4. 运行应用

#### 开发环境
```bash
python run.py
# 或
export FLASK_ENV=development
flask run
```

#### 生产环境
```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务器
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## 环境配置

### 开发环境 (development)
- 自动重载
- 调试器启用
- 详细日志 (DEBUG)

### 生产环境 (production)
- 多进程
- 调试器禁用
- 日志级别 INFO

### 测试环境 (testing)
- 用于单元测试
- 隔离的日志文件

## 配置文件

项目使用 `config/config.json` 统一管理配置：

```json
{
  "development": {
    "app": { "host": "127.0.0.1", "port": 5000 },
    "logging": { "level": "DEBUG" }
  },
  "production": {
    "app": { "host": "0.0.0.0", "port": 5000 },
    "logging": { "level": "INFO" }
  }
}
```

修改配置只需编辑 JSON 文件，无需修改代码。

## 部署到服务器

### 使用 systemd

创建 `/etc/systemd/system/flask-app.service`:

```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/flask-app
Environment="PATH=/var/www/flask-app/env/bin"
ExecStart=/var/www/flask-app/env/bin/gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start flask-app
sudo systemctl enable flask-app
```

### 使用 Docker (可选)

创建 `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

构建和运行：
```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

## 日志管理

日志文件位于 `logs/` 目录：
- `app.log` - 主日志文件
- `trace.log` - 异常追踪日志

查看日志：
```bash
# 实时查看
tail -f logs/app.log

# 查看错误
grep ERROR logs/app.log
```

## 常见问题

### 端口被占用
修改 `config.json` 中的 port 配置

### 权限问题
确保 logs/ 目录可写：
```bash
chmod 755 logs/
```

### 配置不生效
检查 FLASK_ENV 环境变量：
```bash
export FLASK_ENV=production
```
