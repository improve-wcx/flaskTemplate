# Protocol Buffers 在 Flask 中的使用指南

## 概述

本项目使用 Protocol Buffers (protobuf) 作为数据序列化格式，用于定义 Flask Web 接口的请求和响应数据结构。

**重要说明**：本项目**不使用 gRPC**，仅使用 protobuf 进行数据序列化/反序列化。

## 为什么使用 Protocol Buffers？

1. **强类型定义**：在 proto 文件中明确定义数据结构，减少运行时错误
2. **自动验证**：protobuf 自动验证数据格式
3. **类型提示**：生成的 `.pyi` 文件提供 IDE 智能提示
4. **易于扩展**：添加新字段不影响现有代码
5. **高效序列化**：支持二进制格式，节省带宽
6. **跨语言支持**：同一 proto 文件可生成多种语言代码

## 项目结构

```
projectTemplate/
├── proto/                          # Proto 文件目录
│   ├── helloworld.proto           # Hello World 示例（学习用）
│   └── common.proto               # 通用消息定义
├── app/
│   ├── proto/                     # 生成的 Python 代码
│   │   ├── __init__.py
│   │   ├── helloworld_pb2.py      # 生成的消息类
│   │   ├── helloworld_pb2.pyi     # 类型提示文件
│   │   ├── common_pb2.py
│   │   └── common_pb2.pyi
│   └── routes/
│       └── helloworld.py          # Flask 路由示例
├── scripts/
│   └── generate_protobuf.py       # 代码生成脚本
└── Makefile                       # 构建命令
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 查看示例接口

项目包含一个完整的 Hello World Demo，展示了如何在 Flask 中使用 protobuf：

**接口列表：**
- `POST /api/v1/hello` - 简单的问候接口（JSON 格式）
- `POST /api/v1/hello-binary` - 二进制格式接口
- `POST /api/v1/user` - 获取用户信息
- `POST /api/v1/users` - 获取用户列表
- `POST /api/v1/echo` - Echo 接口（通用响应格式）

### 3. 测试接口

```bash
# 启动服务器
python run.py

# 测试 Hello World 接口
curl -X POST http://127.0.0.1:5000/api/v1/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# 响应
{
  "message": "Hello, Alice!",
  "timestamp": "2026-03-16T10:00:00",
  "request_id": "uuid-here"
}
```

## 如何定义新的 Proto 消息

### 步骤 1：编辑 proto 文件

在 `proto/` 目录下创建或编辑 `.proto` 文件：

```protobuf
syntax = "proto3";

package myapp;

// 请求消息
message CreateUserRequest {
  string username = 1;
  string email = 2;
  int32 age = 3;
}

// 响应消息
message CreateUserResponse {
  bool success = 1;
  string user_id = 2;
  string message = 3;
  string request_id = 4;
}
```

### 步骤 2：生成代码

```bash
# 使用 Makefile
make protobuf

# 或使用脚本
python scripts/generate_protobuf.py
```

### 步骤 3：在 Flask 路由中使用

```python
from flask import Blueprint, request, jsonify
from app.proto import myapp_pb2

myapp_bp = Blueprint('myapp', __name__, url_prefix='/api/v1')

@myapp_bp.route('/user', methods=['POST'])
def create_user():
    # 1. 获取 JSON 数据
    json_data = request.get_json()
    
    # 2. 转换为 protobuf 消息
    request_msg = myapp_pb2.CreateUserRequest()
    request_msg.FromDict(json_data)
    
    # 3. 处理业务逻辑
    user_id = create_user_in_db(
        username=request_msg.username,
        email=request_msg.email,
        age=request_msg.age
    )
    
    # 4. 创建响应
    response_msg = myapp_pb2.CreateUserResponse(
        success=True,
        user_id=user_id,
        message="User created successfully"
    )
    
    # 5. 返回 JSON
    return jsonify({
        "success": response_msg.success,
        "user_id": response_msg.user_id,
        "message": response_msg.message
    }), 201
```

## 在 Flask 中使用 Protobuf 的两种方式

### 方式 1：JSON 格式（推荐用于 Web API）

```python
from flask import request, jsonify
from app.proto import helloworld_pb2

@app.route('/hello', methods=['POST'])
def hello():
    # 获取 JSON 数据
    json_data = request.get_json()
    
    # 转换为 protobuf 消息
    request_msg = helloworld_pb2.HelloRequest()
    request_msg.FromDict(json_data)
    
    # 处理...
    name = request_msg.name
    
    # 创建响应
    response_msg = helloworld_pb2.HelloResponse(
        message=f"Hello, {name}!"
    )
    
    # 转换为字典并返回
    return jsonify({
        "message": response_msg.message
    })
```

### 方式 2：二进制格式（适合高性能场景）

```python
from flask import request

@app.route('/hello-binary', methods=['POST'])
def hello_binary():
    # 获取原始二进制数据
    raw_data = request.get_data()
    
    # 反序列化
    request_msg = helloworld_pb2.HelloRequest()
    request_msg.ParseFromString(raw_data)
    
    # 处理...
    
    # 创建响应并序列化
    response_msg = helloworld_pb2.HelloResponse(
        message=f"Hello, {request_msg.name}!"
    )
    
    # 返回二进制数据
    return response_msg.SerializeToString(), 200, {
        'Content-Type': 'application/x-protobuf'
    }
```

## 常用消息类型

### 基本类型

```protobuf
string    // 字符串
int32     // 32 位整数
int64     // 64 位整数
bool      // 布尔值
float     // 浮点数
double    // 双精度浮点数
bytes     // 字节数据
```

### 复合类型

```protobuf
// 重复字段（列表）
repeated string tags = 1;
repeated UserInfo users = 2;

// 映射（字典）
map<string, int32> scores = 1;

// 嵌套消息
message Order {
  string order_id = 1;
  UserInfo buyer = 2;  // 嵌套消息
  repeated OrderItem items = 3;
}
```

### 枚举

```protobuf
enum Status {
  STATUS_UNSPECIFIED = 0;
  STATUS_PENDING = 1;
  STATUS_APPROVED = 2;
  STATUS_REJECTED = 3;
}

message Order {
  Status status = 1;
}
```

## 最佳实践

### 1. 消息命名

- 使用 PascalCase：`CreateUserRequest`, `UserResponse`
- 请求消息以 `Request` 结尾
- 响应消息以 `Response` 结尾

### 2. 字段编号

- 从 1 开始递增
- 1-15 用于频繁使用的字段
- 不要重用已删除字段的编号

### 3. 使用通用响应格式

```protobuf
message CommonResponse {
  StatusCode status_code = 1;
  string message = 2;
  string request_id = 3;
}
```

### 4. 添加 request_id 用于追踪

```protobuf
message MyResponse {
  bool success = 1;
  string data = 2;
  string request_id = 3;  // 用于日志追踪
}
```

## 生成的文件说明

- `*_pb2.py`: 生成的 Python 消息类
- `*_pb2.pyi`: 类型提示文件（IDE 智能提示）

### 类型提示示例

```python
from app.proto import helloworld_pb2

def process_request(req: helloworld_pb2.HelloRequest) -> None:
    # IDE 会提示所有可用字段
    print(req.name)  # 自动补全
    print(req.DESCRIPTOR)  # 类型检查
```

## 常见问题

### Q: 如何添加新字段？

```protobuf
message UserResponse {
  string user_id = 1;
  string username = 2;
  string email = 3;
  // 添加新字段
  optional string phone = 4;  // 使用 optional 表示可选
}
```

重新生成代码后，旧代码仍然可以工作（新字段为默认值）。

### Q: 如何删除字段？

```protobuf
message UserResponse {
  string user_id = 1;
  string username = 2;
  
  // 删除 email 字段，保留编号
  reserved 3;
  reserved "email";
}
```

### Q: 如何兼容旧版本？

- 新字段使用 `optional` 标记
- 不要修改现有字段的编号
- 使用 `reserved` 保留已删除的字段编号

## 参考示例

查看 `app/routes/helloworld.py` 获取完整的实现示例：

- JSON 格式接口
- 二进制格式接口
- 重复字段使用
- 通用响应格式
- 错误处理

## 相关资源

- [Protocol Buffers 语言指南](https://developers.google.com/protocol-buffers/docs/proto3)
- [Python 使用指南](https://developers.google.com/protocol-buffers/docs/pythontutorial)
- [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)
