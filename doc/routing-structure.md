# 路由结构说明

## 概述

本项目采用 Flask Blueprint 架构，将路由按功能模块拆分，便于维护和扩展。

## 路由分类

### 1. 主路由 (`main_bp`)

**前缀**: 无

**用途**: 处理网站的主要页面路由

| 路径 | 方法 | 函数 | 描述 |
|------|------|------|------|
| `/` | GET | `index()` | 首页 - 静态资源展示页 |
| `/hello` | GET | `hello()` | Hello World 演示页 |
| `/demo` | GET | `demo()` | 静态资源演示页 |
| `/favicon.ico` | GET | `favicon()` | 网站图标（返回 204） |

**访问示例**:
```bash
# 访问首页
curl http://127.0.0.1:5000/

# 访问演示页
curl http://127.0.0.1:5000/demo
```

### 2. API 路由 (`api_bp`)

**前缀**: `/api`

**用途**: RESTful API 端点

| 路径 | 方法 | 函数 | 描述 |
|------|------|------|------|
| `/api/health` | GET | `health_check()` | 健康检查 |
| `/api/version` | GET | `version()` | API 版本信息 |
| `/api/apis` | GET | `list_apis()` | 列出所有可用 API |

**访问示例**:
```bash
# 健康检查
curl http://127.0.0.1:5000/api/health

# 获取 API 列表
curl http://127.0.0.1:5000/api/apis
```

### 3. Protobuf 演示路由 (`demo_protobuf_bp`)

**前缀**: `/api/v1/demo`

**用途**: Protocol Buffers 数据序列化演示

| 路径 | 方法 | 函数 | 描述 |
|------|------|------|------|
| `/api/v1/demo/hello` | GET | `hello_get()` | 获取 Hello 响应 |
| `/api/v1/demo/hello` | POST | `hello_post()` | 发送 Hello 请求 |
| `/api/v1/demo/user/<user_id>` | GET | `user_get()` | 获取用户信息 |
| `/api/v1/demo/users` | POST | `users_post()` | 创建用户 |
| `/api/v1/demo/echo` | POST | `echo()` | Echo 演示 |

**访问示例**:
```bash
# GET 请求
curl http://127.0.0.1:5000/api/v1/demo/hello

# POST 请求
curl -X POST http://127.0.0.1:5000/api/v1/demo/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'
```

### 4. 静态资源路由 (`static_bp`)

**前缀**: `/resources`

**用途**: 备用静态资源页面（主要功能已移至 `main_bp`）

| 路径 | 方法 | 函数 | 描述 |
|------|------|------|------|
| `/resources/` | GET | `static_index()` | 静态资源首页（备用） |
| `/resources/demo` | GET | `static_demo()` | 静态资源演示页（备用） |

**注意**: 主要页面路由已移至 `main_bp`，此蓝图仅作为备用。

### 5. 静态文件服务

**前缀**: `/static`

**用途**: Flask 内置的静态文件服务

| 路径 | 方法 | 描述 |
|------|------|------|
| `/static/<path:filename>` | GET | 访问静态文件（CSS/JS/图片等） |

**文件位置**: `app/static/`

**访问示例**:
```bash
# 访问 CSS
curl http://127.0.0.1:5000/static/css/main.css

# 访问图片
curl http://127.0.0.1:5000/static/images/logo.svg
```

## 路由注册顺序

在 `app/__init__.py` 中，蓝图的注册顺序如下：

```python
# 1. 主路由（优先级最高）
app.register_blueprint(main_bp)

# 2. API 路由
app.register_blueprint(api_bp)

# 3. Protobuf 演示路由
app.register_blueprint(demo_protobuf_bp)

# 4. 静态资源路由（备用）
app.register_blueprint(static_bp)
```

## 路由收集机制

项目实现了自动 API 注册机制，在 `app/__init__.py` 中：

```python
def _collect_routes(blueprint, category: str):
    """收集蓝图中的所有路由并注册到 API  registry"""
    # 遍历所有路由规则
    # 过滤出当前蓝图的路由
    # 排除 HEAD/OPTIONS 方法
    # 注册到 _api_registry
```

**分类映射**:
```python
blueprint_categories = {
    'main': '系统',
    'api': '系统',
    'demo_protobuf': 'Protobuf 演示',
    'static_bp': '静态资源',
    'admin': '管理'
}
```

## 最佳实践

### 1. 添加新路由

1. 在对应的 blueprint 文件中添加路由
2. 确保路由命名清晰、符合 RESTful 规范
3. 添加适当的文档字符串
4. 编写单元测试

### 2. 路由优先级

- 更具体的路由应该放在前面
- 避免路由冲突（如 `/demo` 和 `/demo/<id>`）
- 使用蓝图前缀避免命名冲突

### 3. 模板引用

在 Jinja2 模板中使用路由：
```html
<!-- 正确 -->
<a href="{{ url_for('main.index') }}">首页</a>
<a href="{{ url_for('api.list_apis') }}">API 列表</a>

<!-- 静态文件 -->
<img src="{{ url_for('static', filename='images/logo.svg') }}">
```

## 测试

运行路由测试：
```bash
# 运行所有测试
pytest tests/ -v

# 仅运行主路由测试
pytest tests/test_routes/test_main.py -v

# 仅运行 API 测试
pytest tests/test_routes/test_api.py -v
```

## 变更历史

### 2026-03-16

- **重构**: 将首页从 `/` 返回 "Hello, World!" 改为渲染 `index.html`
- **新增**: `/hello` 路由用于 Hello World 演示
- **新增**: `/demo` 路由用于静态资源演示
- **调整**: `static_bp` 前缀从 `/static-pages` 改为 `/resources`（备用）
- **更新**: 所有模板导航链接指向新路由
- **新增**: 完整的单元测试覆盖

## 相关文档

- [路由开发指南](../routes/development.md)
- [API 设计规范](../api/README.md)
- [模板系统](../templates/README.md)
- [静态资源管理](../static/README.md)
