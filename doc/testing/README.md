# 测试指南

## 测试结构

```
tests/
├── conftest.py           # pytest 配置
├── test_routes/          # 路由测试
│   ├── test_main.py
│   ├── test_api.py
│   └── test_users.py
└── test_config/          # 配置测试
    └── test_loader.py
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定文件
pytest tests/test_routes/test_main.py -v

# 运行特定函数
pytest tests/test_routes/test_main.py::test_hello -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html

# 查看报告
open htmlcov/index.html
```

## 编写测试

### 基本测试

```python
def test_hello_route(client):
    """测试首页路由"""
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Hello' in resp.data
```

### 测试 API

```python
import json

def test_create_user(client):
    """测试创建用户 API"""
    data = {'name': 'Alice'}
    resp = client.post(
        '/api/users/',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert resp.status_code == 201
    result = resp.get_json()
    assert result['data']['name'] == 'Alice'
```

### 使用 Fixture

```python
@pytest.fixture
def sample_user():
    """提供示例用户"""
    return User(1, 'Alice', 'alice@example.com')

def test_user_to_dict(sample_user):
    """测试用户模型"""
    result = sample_user.to_dict()
    assert result['name'] == 'Alice'
```

## 测试覆盖

### 路由测试
- 测试所有 HTTP 方法
- 测试各种状态码
- 测试错误处理

### 配置测试
- 测试各环境配置
- 测试配置加载
- 测试配置值获取

### 服务层测试
- 测试业务逻辑
- 测试边界条件
- 测试异常处理

## 最佳实践

1. **测试命名** - 清晰描述测试内容
2. **单一职责** - 每个测试只测一件事
3. **独立测试** - 测试之间不依赖
4. **使用 Fixture** - 复用测试数据
5. **断言明确** - 清晰的断言信息
6. **覆盖边界** - 测试边界情况
7. **持续集成** - 每次提交都运行测试
