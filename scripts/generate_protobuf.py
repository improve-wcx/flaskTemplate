#!/usr/bin/env python3
"""
Protocol Buffers 代码生成脚本 (Python 版本)
不依赖系统安装的 protoc，使用 Python 的 grpc_tools 模块
"""

import os
import sys
import subprocess
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
    
    print_color("=" * 40, Colors.GREEN)
    print_color("Protocol Buffers 代码生成", Colors.GREEN)
    print_color("=" * 40, Colors.GREEN)
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
    print()
    
    # 构建 protoc 命令
    proto_paths = [str(proto_dir)]
    python_out = str(output_dir)
    grpc_python_out = str(output_dir)
    
    # 使用 grpc_tools.protoc 的主函数
    try:
        from grpc_tools import protoc
        
        for proto_file in proto_files:
            filename = proto_file.name
            print_color(f"处理：{filename}", Colors.YELLOW)
            
            result = protoc.main(
                [
                    '',
                    f'-I{proto_dir}',
                    f'--python_out={python_out}',
                    f'--grpc_python_out={grpc_python_out}',
                    f'--mypy_out={python_out}',
                    f'--mypy_grpc_out={python_out}',
                    str(proto_file)
                ]
            )
            
            if result == 0:
                print_color(f"  ✓ 生成成功", Colors.GREEN)
            else:
                print_color(f"  ✗ 生成失败", Colors.RED)
                return 1
        
        print()
        print_color("=" * 40, Colors.GREEN)
        print_color("代码生成完成!", Colors.GREEN)
        print_color("=" * 40, Colors.GREEN)
        print()
        
        # 显示生成的文件
        print_color("生成的文件:", Colors.GREEN)
        py_files = sorted(output_dir.glob("*.py"))
        pyi_files = sorted(output_dir.glob("*.pyi"))
        
        for f in py_files:
            print(f"  - {f.name}")
        
        if pyi_files:
            print_color("  类型提示文件:", Colors.GREEN)
            for f in pyi_files:
                print(f"    - {f.name}")
        
        print()
        print_color("提示:", Colors.YELLOW)
        print("  - .py 文件是生成的 Python 代码")
        print("  - .pyi 文件是类型提示文件")
        print("  - _grpc.py 文件是 gRPC 服务 stub")
        print()
        print("  导入示例:")
        print("    from app.proto import user_service_pb2")
        print("    from app.proto import user_service_pb2_grpc")
        
        return 0
        
    except ImportError:
        print_color("错误：grpcio-tools 未安装", Colors.RED)
        print_color("请运行：pip install grpcio-tools mypy-protobuf", Colors.YELLOW)
        return 1
    except Exception as e:
        print_color(f"错误：{e}", Colors.RED)
        return 1

if __name__ == "__main__":
    sys.exit(main())
