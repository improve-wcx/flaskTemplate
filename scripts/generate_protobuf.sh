#!/bin/bash

# Protocol Buffers 代码生成脚本
# 生成 Python 代码和对应的 .pyi 类型提示文件

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTO_DIR="${PROJECT_ROOT}/proto"
OUTPUT_DIR="${PROJECT_ROOT}/app/proto"

# 检查 protoc 是否安装
if ! command -v protoc &> /dev/null; then
    echo -e "${RED}错误：protoc 未安装${NC}"
    echo "请安装 Protocol Buffers 编译器:"
    echo "  Ubuntu/Debian: sudo apt-get install protobuf-compiler"
    echo "  macOS: brew install protobuf"
    echo "  或者访问：https://github.com/protocolbuffers/protobuf/releases"
    exit 1
fi

# 检查 grpcio-tools 是否安装
if ! python3 -c "import grpc_tools" 2>/dev/null; then
    echo -e "${RED}错误：grpcio-tools 未安装${NC}"
    echo "请运行：pip install grpcio-tools"
    exit 1
fi

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Protocol Buffers 代码生成${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# 创建输出目录
mkdir -p "${OUTPUT_DIR}"

# 创建 __init__.py 文件
touch "${OUTPUT_DIR}/__init__.py"

# 查找所有 .proto 文件
PROTO_FILES=$(find "${PROTO_DIR}" -name "*.proto" -type f)

if [ -z "${PROTO_FILES}" ]; then
    echo -e "${YELLOW}警告：在 ${PROTO_DIR} 中未找到 .proto 文件${NC}"
    exit 0
fi

echo -e "${GREEN}正在生成代码...${NC}"
echo ""

# 为每个 proto 文件生成代码
for proto_file in ${PROTO_FILES}; do
    filename=$(basename "${proto_file}" .proto)
    echo -e "${YELLOW}处理：${filename}.proto${NC}"
    
    # 生成 Python 代码和 gRPC 代码
    python3 -m grpc_tools.protoc \
        -I${PROTO_DIR} \
        --python_out=${OUTPUT_DIR} \
        --grpc_python_out=${OUTPUT_DIR} \
        --mypy_out=${OUTPUT_DIR} \
        --mypy_grpc_out=${OUTPUT_DIR} \
        "${proto_file}"
    
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓ 生成成功${NC}"
    else
        echo -e "  ${RED}✗ 生成失败${NC}"
        exit 1
    fi
done

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}代码生成完成！${NC}"
echo -e "${GREEN}输出目录：${OUTPUT_DIR}${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# 显示生成的文件
echo -e "${GREEN}生成的文件:${NC}"
find "${OUTPUT_DIR}" -name "*.py*" -type f | sort | while read file; do
    echo "  - $(basename ${file})"
done

echo ""
echo -e "${YELLOW}提示:${NC}"
echo "  - .py 文件是生成的 Python 代码"
echo "  - .pyi 文件是类型提示文件 (由 mypy 插件生成)"
echo "  - _grpc.py 文件是 gRPC 服务 stub"
echo ""
echo "  在代码中导入示例:"
echo "    from app.proto import user_service_pb2"
echo "    from app.proto import user_service_pb2_grpc"
