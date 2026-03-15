# Flask Project Template

一个结构化的 Flask 项目模板，支持模块化开发和多环境配置。

## 项目结构

```
projectTemplate/
├── app/                    # 主应用包
│   ├── __init__.py        # 应用工厂
│   ├── routes/            # 路由模块
│   │   ├── main.py        # 主路由
│   │   ├── api.py         # API 路由
│   │   └── admin.py       # 管理后台路由
│   ├── models/            # 数据模型（待扩展）
│   ├── services/          # 业务逻辑层（待扩展）
│   ├── templates/         # HTML 模板
│   └── static/            # 静态文件
├── config/                # 配置文件
│   ├── base.py           # 基础配置
│   ├── development.py    # 开发环境
│   ├── testing.py        # 测试环境
│   └── production.py     # 生产环境
├── utils/                 # 工具函数
│   └── logger.py         # 日志配置
├── tests/                 # 测试目录
│   ├── conftest.py       # pytest 配置
│   └── test_routes/      # 路由测试
├── logs/                  # 日志目录（gitignore 排除）
├── run.py                 # 启动入口
├── wsgi.py                # WSGI 入口
├── requirements.txt       # 依赖
└── .env.example          # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv env
source env/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements-dev.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

### 3. 运行应用

```bash
# 开发模式
python run.py
```

### 4. 运行测试

```bash
pytest tests/ -v
```

## 功能特性

- 模块化路由管理
- JSON 格式结构化日志
- 多环境配置支持
- 完整的测试套件

## 技术栈

- Flask 2.3.3
- Python 3.12
- pytest 9.0
