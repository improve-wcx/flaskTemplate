#!/usr/bin/env python3
"""
Protocol Buffers 代码生成脚本 (Python 版本)
仅生成 Python 消息类，不生成 gRPC 代码
"""

import os
import sys
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def print_color(message, color):
    print(f"{color}{message}{Colors.NC}")

def main():
    project_root = Path(__file__).parent.parent
    proto_dir = project_root / "proto"
    output_dir = project_root / "app" / "proto"
    
    print_color("=" * 50, Colors.GREEN)
    print_color("Protocol Buffers 代码生成", Colors.GREEN)
    print_color("=" * 50, Colors.GREEN)
    print()
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 __init__.py
    (output_dir / "__init__.py").touch()
    
    # 查找所有 proto 文件
    proto_files = list(proto_dir.glob("*.proto"))
    
    if not proto_files:
        print_color(f"警告：在 {proto_dir} 中未找到 .proto 文件", Colors.YELLOW)
        return 0
    
    print_color(f"找到 {len(proto_files)} 个 proto 文件", Colors.GREEN)
    for pf in proto_files:
        print_color(f"  - {pf.name}", Colors.YELLOW)
    print()
    
    # 使用 protoc 生成 Python 代码和类型提示
    try:
        from grpc_tools import protoc
        
        proto_paths = [str(proto_dir)]
        python_out = str(output_dir)
        
        for proto_file in proto_files:
            filename = proto_file.name
            print_color(f"处理：{filename}", Colors.YELLOW)
            
            # 构建参数列表
            args = [
                '',
                f'-I{proto_dir}',
                f'--python_out={python_out}',
                f'--mypy_out={python_out}',
                str(proto_file)
            ]
            
            result = protoc.main(args)
            
            if result == 0:
                print_color(f"  ✓ 生成成功", Colors.GREEN)
            else:
                print_color(f"  ✗ 生成失败", Colors.RED)
                return 1
        
        print()
        print_color("=" * 50, Colors.GREEN)
        print_color("代码生成完成!", Colors.GREEN)
        print_color("=" * 50, Colors.GREEN)
        print()
        
        # 显示生成的文件
        print_color("生成的文件:", Colors.GREEN)
        py_files = sorted(output_dir.glob("*_pb2.py"))
        pyi_files = sorted(output_dir.glob("*_pb2.pyi"))
        
        for f in py_files:
            print(f"  - {f.name}")
        
        if pyi_files:
            print_color("\n类型提示文件:", Colors.GREEN)
            for f in pyi_files:
                print(f"    - {f.name}")
        
        print()
        print_color("提示:", Colors.YELLOW)
        print("  - .py 文件是生成的 Python 消息类")
        print("  - .pyi 文件是类型提示文件（用于 IDE 智能提示）")
        print()
        print("  在 Flask 中使用示例:")
        print("    from app.proto import demo_pb2")
        print("    ")
        print("    # 解析请求数据")
        print("    request = demo_pb2.HelloRequest()")
        print("    request.ParseFromString(request_data)")
        print("    ")
        print("    # 创建响应")
        print("    response = demo_pb2.HelloResponse(")
        print("        message=f'Hello, {request.name}!',")
        print("        timestamp=...")
        print("    )")
        print("    response_data = response.SerializeToString()")
        
        return 0
        
    except ImportError:
        print_color("错误：需要安装 grpcio-tools", Colors.RED)
        print_color("请运行：pip install grpcio-tools mypy-protobuf", Colors.YELLOW)
        return 1
    except Exception as e:
        print_color(f"错误：{e}", Colors.RED)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
