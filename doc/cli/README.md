# 命令行客户端使用指南

## 概述

`cli.py` 是一个功能完整的命令行客户端，用于调用所有 Web API 接口。它提供了与 Web API 相同的功能，方便在终端、脚本和自动化场景中使用。

## 安装

无需额外安装，直接使用即可：

```bash
# 确保在虚拟环境中
source env/bin/activate

# 运行客户端
python cli.py --help
```

## 基本用法

### 查看所有可用命令

```bash
python cli.py --help
```

输出示例：
```
usage: cli.py [-h] [--base-url BASE_URL] {health,version,hello,user,users,echo,admin,home} ...

Web API 命令行客户端 - 调用所有 Web API 接口

positional arguments:
  {health,version,hello,user,users,echo,admin,home}
                        可用命令
    health              健康检查
    version             版本信息
    hello               问候接口
    user                获取用户信息
    users               获取用户列表
    echo                Echo 接口
    admin               管理后台
    home                首页

options:
  -h, --help            show this help message and exit
  --base-url BASE_URL, -b BASE_URL
                        API 基础 URL (默认：http://127.0.0.1:5000)

示例:
  python cli.py health
  python cli.py hello --post --name "Alice"
  python user 12345
  python cli.py users --page 1 --page-size 10
  python cli.py echo --data '{"key": "value"}'
```

### 查看特定命令帮助

```bash
python cli.py hello --help
python cli.py users --help
python cli.py echo --help
```

## 全局参数

### `--base-url`, `-b`

指定 API 服务器的基础 URL。

```bash
# 使用默认地址 (http://127.0.0.1:5000)
python cli.py health

# 指定其他地址
python cli.py -b http://localhost:5000 health
python cli.py --base-url http://api.example.com version
```

## 命令详解

### 1. health - 健康检查

检查服务器是否正常运行。

```bash
# 基本用法
python cli.py health

# 指定服务器
python cli.py -b http://localhost:5000 health
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/health
状态码：200
--------------------------------------------------
{
  "status": "healthy",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**参数：** 无

---

### 2. version - 版本信息

获取 API 版本信息。

```bash
# 基本用法
python cli.py version
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/version
状态码：200
--------------------------------------------------
{
  "version": "1.0.0",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**参数：** 无

---

### 3. hello - 问候接口

演示 GET 和 POST 两种请求方式。

#### GET 方法

```bash
python cli.py hello --get
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/v1/demo/hello
方法：GET
--------------------------------------------------
{
  "message": "Hello, World!",
  "timestamp": "2026-03-16T10:00:00",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

#### POST 方法

```bash
# 默认问候
python cli.py hello --post

# 指定姓名
python cli.py hello --post --name "Alice"
python cli.py hello --post -n "Bob"
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/v1/demo/hello
方法：POST
请求数据：{'name': 'Alice'}
--------------------------------------------------
{
  "message": "Hello, Alice!",
  "timestamp": "2026-03-16T10:00:00",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**参数：**
- `--get` - 使用 GET 方法（与 `--post` 互斥）
- `--post` - 使用 POST 方法（与 `--get` 互斥）
- `--name`, `-n` - 姓名（仅 POST 有效）

---

### 4. user - 获取用户信息

根据用户 ID 获取详细信息。

```bash
# 获取用户 ID 为 12345 的信息
python cli.py user 12345

# 获取其他用户
python cli.py user 99999
```

**输出示例（成功）：**
```
URL: http://127.0.0.1:5000/api/v1/demo/user/12345
方法：GET
--------------------------------------------------
{
  "success": true,
  "user": {
    "userId": "12345",
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25
  },
  "message": "User found",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**输出示例（用户不存在）：**
```
URL: http://127.0.0.1:5000/api/v1/demo/user/99999
方法：GET
--------------------------------------------------
{
  "success": false,
  "message": "User 99999 not found",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**参数：**
- `user_id` (必需) - 用户 ID

---

### 5. users - 获取用户列表

获取分页用户列表。

```bash
# 默认参数（第 1 页，每页 10 条）
python cli.py users

# 指定页码和每页数量
python cli.py users --page 2 --page-size 20
python cli.py users -p 2 -s 20
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/v1/demo/users
方法：POST
请求数据：{'page': 2, 'page_size': 20}
--------------------------------------------------
{
  "success": true,
  "users": [
    {
      "userId": "21",
      "username": "user_21",
      "email": "user21@example.com",
      "age": 21
    },
    ...
  ],
  "total": 100,
  "page": 2,
  "pageSize": 20,
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4"
}
```

**参数：**
- `--page`, `-p` - 页码（默认：1）
- `--page-size`, `-s` - 每页数量（默认：10）

---

### 6. echo - Echo 接口

发送任意 JSON 数据并返回，用于测试。

```bash
# 发送简单数据
python cli.py echo --data '{"key": "value"}'

# 发送复杂数据
python cli.py echo -d '{"name": "Alice", "age": 25, "city": "Beijing"}'

# 发送空数据
python cli.py echo
```

**输出示例：**
```
URL: http://127.0.0.1:5000/api/v1/demo/echo
方法：POST
请求数据：{'key': 'value'}
--------------------------------------------------
{
  "statusCode": 0,
  "message": "Echo successful",
  "request_id": "1548b98b-0ac0-4ce4-960f-12ba556ec0a4",
  "echo_data": {
    "key": "value"
  }
}
```

**参数：**
- `--data`, `-d` - JSON 数据（字符串格式）

---

### 7. admin - 管理后台

访问管理后台（当前仅显示信息）。

```bash
python cli.py admin
```

**输出：**
```
URL: http://127.0.0.1:5000/admin/
方法：GET
--------------------------------------------------
注意：管理后台尚未实现完整功能
```

**参数：** 无

---

### 8. home - 首页

访问网站首页。

```bash
python cli.py home
```

**输出示例：**
```
URL: http://127.0.0.1:5000/
方法：GET
--------------------------------------------------
状态码：200
内容：Hello, World!
```

**参数：** 无

---

## 使用场景

### 1. 快速测试

```bash
# 检查服务是否正常
python cli.py health

# 测试 API 响应
python cli.py hello --post --name "Test"
```

### 2. 脚本自动化

```bash
#!/bin/bash
# 批量获取用户信息
for user_id in 12345 67890 11111; do
    echo "=== 用户 $user_id ==="
    python cli.py user $user_id
    echo ""
done
```

### 3. 集成到 CI/CD

```bash
# 健康检查脚本
#!/bin/bash
response=$(python cli.py health 2>&1)
if echo "$response" | grep -q '"status": "healthy"'; then
    echo "✓ 服务健康检查通过"
    exit 0
else
    echo "✗ 服务健康检查失败"
    exit 1
fi
```

### 4. 数据导出

```bash
# 导出所有用户
python cli.py users --page 1 --page-size 100 > users_page1.json
python cli.py users --page 2 --page-size 100 > users_page2.json
```

### 5. 性能测试

```bash
# 简单性能测试
for i in {1..100}; do
    python cli.py health > /dev/null
done
echo "完成 100 次请求"
```

## 错误处理

客户端会自动处理以下错误：

1. **连接错误** - 服务器不可达
2. **HTTP 错误** - 4xx, 5xx 响应
3. **JSON 解析错误** - 响应格式错误
4. **超时错误** - 请求超时（默认 30 秒）

**错误输出示例：**
```
URL: http://localhost:9999/health
状态码：None
--------------------------------------------------
{
  "error": "无法连接到服务器：Connection refused"
}
```

## 返回码

- `0` - 成功
- `1` - 失败（HTTP 错误、连接错误等）

## 高级技巧

### 1. 结合 jq 处理 JSON

```bash
# 只提取特定字段
python cli.py health | jq '.status'

# 格式化输出
python cli.py users | jq '.users[].username'
```

### 2. 在 Python 脚本中调用

```python
import subprocess
import json

# 调用客户端
result = subprocess.run(
    ['python', 'cli.py', 'health'],
    capture_output=True,
    text=True
)

# 解析输出
data = json.loads(result.stdout.split('\n', 4)[-1])
print(data)
```

### 3. 批量操作

```bash
# 批量创建和查询用户
for i in {1..10}; do
    python cli.py echo -d "{\"user_id\": $i, \"action\": \"create\"}"
done
```

## 常见问题

### Q: 如何连接到远程服务器？

```bash
python cli.py -b http://remote-server.com:5000 health
```

### Q: 如何保存输出到文件？

```bash
python cli.py users > users.json
python cli.py hello --post -n "Alice" > hello_response.json
```

### Q: 如何查看详细的请求信息？

客户端会自动显示 URL、方法和请求数据，无需额外参数。

### Q: 是否支持代理？

当前版本不支持代理。如需代理支持，请设置环境变量：

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
python cli.py health
```

## 扩展客户端

如需添加新命令，请参考 `cli.py` 源码结构：

1. 添加新的 `cmd_xxx` 函数
2. 在 `main()` 中添加子命令解析器
3. 更新文档

详细实现请参考 `cli.py` 文件注释。

## 相关文档

- [路由模块说明](../routes/README.md)
- [Protobuf 使用指南](../protobuf/README.md)
- [日志系统说明](../log/README.md)
