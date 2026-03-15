# Protocol Buffers 在 Flask 中的使用

## 概述

本目录包含在 Flask Web 项目中使用 Protocol Buffers (protobuf) 进行数据序列化的完整指南。

**重要说明**：本项目**不使用 gRPC**，仅使用 protobuf 进行数据序列化/反序列化。

## 文档列表

- [📖 使用指南](README.md) - Protocol Buffers 在 Flask 中的完整使用指南

## 快速开始

### 为什么使用 Protocol Buffers？

1. **强类型定义**：在 proto 文件中明确定义数据结构
2. **自动验证**：protobuf 自动验证数据格式
3. **类型提示**：生成的 `.pyi` 文件提供 IDE 智能提示
4. **易于扩展**：添加新字段不影响现有代码
5. **高效序列化**：支持二进制格式，节省带宽
6. **跨语言支持**：同一 proto 文件可生成多种语言代码

### 项目结构

```
projectTemplate/
├── proto/                          # Proto 文件目录
│   ├── helloworld.proto           # Hello World 示例
│   └── common.proto               # 通用消息定义
├── app/
│   ├── proto/                     # 生成的 Python 代码
│   │   ├── helloworld_pb2.py
│   │   ├── helloworld_pb2.pyi
│   │   ├── common_pb2.py
│   │   └── common_pb2.pyi
│   └── routes/
│       └── helloworld.py          # Flask 路由示例
└── doc/protobuf/                  # 本文档目录
    └── README.md                  # 使用指南
```

### 快速示例

#### 1. 定义 proto 文件

```protobuf
syntax = "proto3";

package helloworld;

message HelloRequest {
  string name = 1;
}

message HelloResponse {
  string message = 1;
  string timestamp = 2;
  string request_id = 3;
}
```

#### 2. 生成 Python 代码

```bash
python scripts/generate_protobuf.py
```

#### 3. 在 Flask 中使用

```python
from flask import request, jsonify
from app.proto import helloworld_pb2
from google.protobuf.json_format import ParseDict, MessageToDict

@app.route('/api/v1/hello', methods=['POST'])
def hello():
    json_data = request.get_json()
    
    # JSON -> Protobuf
    request_msg = helloworld_pb2.HelloRequest()
    ParseDict(json_data, request_msg)
    
    # 处理业务逻辑
    name = request_msg.name if request_msg.name else "World"
    response_msg = helloworld_pb2.HelloResponse(
        message=f"Hello, {name}!",
        timestamp=datetime.now().isoformat(),
        request_id=generate_request_id()
    )
    
    # Protobuf -> JSON
    return jsonify(MessageToDict(response_msg))
```

## 核心概念

### JSON 与 Protobuf 转换

使用 `google.protobuf.json_format` 模块：

```python
from google.protobuf.json_format import ParseDict, MessageToDict

# JSON -> Protobuf
request_msg = helloworld_pb2.HelloRequest()
ParseDict({"name": "Alice"}, request_msg)

# Protobuf -> JSON
response_dict = MessageToDict(response_msg)
```

### 二进制格式

```python
# 序列化
binary_data = response_msg.SerializeToString()

# 反序列化
request_msg = helloworld_pb2.HelloRequest()
request_msg.ParseFromString(binary_data)
```

### 常用消息类型

- **基础类型**: string, int32, int64, bool, float, double
- **复合类型**: message (嵌套消息)
- **重复字段**: repeated field (数组)
- **映射字段**: map<key_type, value_type>

## 示例接口

项目包含完整的 Hello World Demo：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/hello` | POST | JSON 格式问候 |
| `/api/v1/hello-binary` | POST | 二进制格式问候 |
| `/api/v1/user` | POST | 获取用户信息 |
| `/api/v1/users` | POST | 获取用户列表 (repeated 字段) |
| `/api/v1/echo` | POST | Echo 接口 (通用响应) |

## 最佳实践

1. **命名规范**：
   - proto 文件使用 `snake_case`
   - 消息名使用 `PascalCase`
   - 字段名使用 `snake_case`

2. **字段编号**：
   - 从 1 开始编号
   - 不要使用 19000-19999（保留给 protobuf 内部使用）
   - 已使用的编号不要更改

3. **向后兼容**：
   - 不要删除已有字段，可以标记为 `deprecated`
   - 新字段使用可选的编号
   - 不要改变已有字段的编号

4. **文档注释**：
   - 为每个消息和字段添加注释
   - 说明字段的用途和格式要求

## 相关文档

- [日志系统文档](../log/README.md) - 日志格式和 Request ID 追踪
- [API 接口文档](../api/README.md) - API 设计规范
- [路由开发指南](../routes/development.md) - 如何添加新路由

## 常见问题

### Q: 为什么不使用 gRPC？

A: 本项目只需要数据序列化功能，不需要 RPC 调用。使用 protobuf 单独进行序列化更轻量。

### Q: JSON 字段名是 camelCase 还是 snake_case？

A: `MessageToDict` 默认将 `snake_case` 转换为 `camelCase`。如果需要保持 `snake_case`，可以设置参数：

```python
MessageToDict(msg, preserving_proto_field_name=True)
```

### Q: 如何处理嵌套消息？

A: 嵌套消息会自动转换：

```protobuf
message User {
  string user_id = 1;
  Profile profile = 2;
}

message Profile {
  string name = 1;
  string email = 2;
}
```

转换为 JSON：

```json
{
  "userId": "123",
  "profile": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

## 更新日志

- 2026-03-16: 初始版本，包含 Hello World Demo 和完整使用指南
