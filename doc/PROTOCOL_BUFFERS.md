# Protocol Buffers 使用指南

## 概述

本项目使用 Protocol Buffers (protobuf) 作为接口定义语言 (IDL)，用于定义请求和响应消息格式，以及 gRPC 服务接口。

## 安装

### 1. 安装 Protocol Buffers 编译器 (protoc)

**Ubuntu/Debian:**
```bash
sudo apt-get install protobuf-compiler
```

**macOS:**
```bash
brew install protobuf
```

**Windows:**
下载预编译的二进制文件: https://github.com/protocolbuffers/protobuf/releases

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

或单独安装:
```bash
pip install protobuf grpcio grpcio-tools mypy-protobuf
```

## 项目结构

```
projectTemplate/
├── proto/                          # Proto 文件目录
│   ├── user_service.proto         # 用户服务定义
│   ├── auth_service.proto         # 认证服务定义
│   └── common.proto               # 通用消息定义
├── app/
│   └── proto/                     # 生成的 Python 代码目录
│       ├── __init__.py
│       ├── user_service_pb2.py    # 生成的消息类
│       ├── user_service_pb2.pyi   # 类型提示文件
│       ├── user_service_pb2_grpc.py  # gRPC 服务 stub
│       └── ...
├── scripts/
│   └── generate_protobuf.sh       # 代码生成脚本
└── Makefile                       # 构建命令
```

## 使用

### 生成代码

**使用 Makefile:**
```bash
# 生成代码
make protobuf

# 清理生成的代码
make protobuf-clean

# 重新生成代码
make protobuf-regenerate

# 检查环境
make protobuf-check
```

**使用脚本:**
```bash
./scripts/generate_protobuf.sh
```

### 生成的文件说明

- `*_pb2.py`: 生成的 Python 消息类
- `*_pb2.pyi`: 类型提示文件 (用于 IDE 智能提示和类型检查)
- `*_pb2_grpc.py`: gRPC 服务客户端和服务端 stub

### 在代码中使用

```python
from app.proto import user_service_pb2
from app.proto import user_service_pb2_grpc

# 创建请求消息
request = user_service_pb2.UserRequest(
    user_id="123",
    username="john_doe",
    email="john@example.com",
    roles=["admin", "user"]
)

# 访问消息字段
print(f"User ID: {request.user_id}")
print(f"Username: {request.username}")

# 创建 gRPC 客户端
# stub = user_service_pb2_grpc.UserServiceStub(channel)
# response = stub.GetUser(request)
```

## Proto 文件规范

### 消息定义

```protobuf
message UserRequest {
  string user_id = 1;
  string username = 2;
  string email = 3;
  repeated string roles = 4;
}
```

### 枚举定义

```protobuf
enum StatusCode {
  STATUS_CODE_UNSPECIFIED = 0;
  STATUS_CODE_SUCCESS = 1;
  STATUS_CODE_FAILURE = 2;
}
```

### 服务定义

```protobuf
service UserService {
  rpc GetUser(UserRequest) returns (UserResponse);
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
}
```

### 最佳实践

1. **命名规范**
   - 消息名使用 PascalCase: `UserRequest`
   - 字段名使用 snake_case: `user_id`
   - 服务名使用 PascalCase: `UserService`
   - RPC 方法使用 PascalCase: `GetUser`

2. **字段编号**
   - 从 1 开始递增
   - 1-15 用于频繁使用的字段 (占用 1 字节)
   - 16-2047 用于不频繁使用的字段 (占用 2 字节)
   - 不要重用已删除字段的编号

3. **消息设计**
   - 为每个消息添加注释
   - 使用 `repeated` 表示列表
   - 使用 `map` 表示字典
   - 考虑使用 `oneof` 表示互斥字段

4. **版本控制**
   - 不要修改现有字段的编号
   - 不要修改现有字段的类型
   - 新字段添加新的编号
   - 已删除字段保留编号 (标记为 reserved)

## 类型提示 (.pyi 文件)

生成的 `.pyi` 文件提供以下好处:

1. **IDE 智能提示**: 在 VS Code、PyCharm 等编辑器中获得自动补全
2. **类型检查**: 使用 mypy 进行静态类型检查
3. **代码文档**: 明确显示消息字段和类型

### 使用类型提示

```python
from app.proto import user_service_pb2

def process_user(request: user_service_pb2.UserRequest) -> None:
    # IDE 会提示 request 的所有可用字段
    print(request.user_id)
    print(request.username)
```

### 运行类型检查

```bash
# 安装 mypy
pip install mypy

# 运行类型检查
mypy app/
```

## 常见问题

### Q: 如何添加新的 proto 文件？

1. 在 `proto/` 目录下创建新的 `.proto` 文件
2. 定义消息和服务
3. 运行 `make protobuf` 生成代码
4. 在代码中导入生成的模块

### Q: 如何修改现有的 proto 文件？

1. 修改 `.proto` 文件
2. 运行 `make protobuf-regenerate` 重新生成代码
3. 更新使用这些消息的代码

### Q: 生成的代码应该提交到 git 吗？

建议:
- **开发环境**: 不提交，每次构建时生成
- **生产环境**: 可以提交，避免部署时需要 protoc

本项目配置为不提交生成的代码，在 `.gitignore` 中已排除 `app/proto/*.py`

### Q: 如何处理 proto 文件版本兼容性？

- 使用 `reserved` 保留已删除的字段编号
- 使用 `optional` 标记可选字段 (proto3)
- 保持向后兼容的字段类型转换

## 参考资源

- [Protocol Buffers 官方文档](https://developers.google.com/protocol-buffers)
- [Proto3 语言指南](https://developers.google.com/protocol-buffers/docs/proto3)
- [gRPC Python 快速开始](https://grpc.io/docs/languages/python/quickstart/)
- [mypy-protobuf 插件](https://github.com/nipunn1313/mypy-protobuf)
