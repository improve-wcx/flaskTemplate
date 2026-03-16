# 服务层说明

## 当前状态

本项目提供了服务层的基础架构示例，但尚未实现具体的业务逻辑层。

### 已提供的服务

- **BaseService** (`app/services/base.py`) - 基础服务类，提供 request_id 日志支持
- **TextSubmissionService** (`app/services/text_submission.py`) - 文本提交存储服务
  - 支持富文本内容存储
  - 提供分页和搜索功能
  - 线程安全的文件持久化
- 示例展示了如何在服务层使用结构化日志

### 规划中的服务

- UserService - 用户服务
- ProductService - 产品服务  
- OrderService - 订单服务

## 开发指南

### 如何创建服务类

参考 `app/services/base.py` 中的 `BaseService` 示例：

```python
from app.services.base import BaseService
from utils.logger import get_request_id

class UserService(BaseService):
    """用户服务类"""
    
    def __init__(self):
        super().__init__('user_service')
    
    def get_user(self, user_id: str):
        """获取用户信息"""
        self.logger.info(f"Getting user {user_id}")
        # 实现逻辑
        return {"id": user_id, "name": "Test User"}
```

### 最佳实践

1. **继承 BaseService** - 获得 request_id 日志支持
2. **使用结构化日志** - 通过 `log_with_request_id()` 方法记录日志
3. **异常处理** - 在服务层统一处理异常
4. **依赖注入** - 通过构造函数注入依赖
