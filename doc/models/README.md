# 数据模型说明

## 当前状态

本项目尚未实现数据模型层。当前版本使用：
- 内存数据结构（字典、列表）
- 外部 API 响应数据
- Protocol Buffers 消息对象

## 规划中的模型

- User - 用户模型
- Product - 产品模型  
- Order - 订单模型

## 开发指南

### 何时需要数据模型

当项目需要持久化数据时，可以考虑引入：

1. **SQLAlchemy** - 关系型数据库 ORM
2. **MongoDB + PyMongo** - 文档数据库
3. **Redis** - 缓存和会话存储
4. **SQLite** - 轻量级嵌入式数据库

### 模型设计原则

1. **单一职责** - 每个模型只负责一个实体的数据
2. **数据验证** - 使用类型注解和验证库（如 pydantic）
3. **序列化/反序列化** - 支持 JSON 转换
4. **关系管理** - 正确处理模型间的关系

### 示例（SQLAlchemy）

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```
