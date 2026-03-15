# 快速开始

## 5 分钟上手

### 1. 安装 (2 分钟)

```bash
# 创建虚拟环境
python3 -m venv env
source env/bin/activate

# 安装依赖
pip install -r requirements-dev.txt
```

### 2. 运行 (1 分钟)

```bash
# 开发模式
python run.py
```

访问 http://127.0.0.1:5000

### 3. 测试 (1 分钟)

```bash
pytest tests/ -v
```

## 验证安装

```bash
# 检查 Python 版本
python --version  # 应 >= 3.12

# 检查依赖
pip list | grep Flask  # 应显示 Flask 2.3.3

# 运行健康检查
curl http://127.0.0.1:5000/api/health
# 返回：{"status": "healthy"}
```

## 下一步

- [查看路由开发指南](../routes/development.md)
- [了解 API 设计](../api/README.md)
- [编写单元测试](../testing/README.md)

## 常见问题

**Q: 端口 5000 被占用怎么办？**

A: 修改 `config/config.json`:
```json
{
  "development": {
    "app": { "port": 5001 }
  }
}
```

**Q: 如何查看日志？**

A: 
```bash
tail -f logs/app.log
```

**Q: 如何切换环境？**

A: 
```bash
export FLASK_ENV=production
python run.py
```
