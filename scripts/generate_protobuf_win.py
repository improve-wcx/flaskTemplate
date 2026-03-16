#!/usr/bin/env python3
"""
Protocol Buffers 代码生成脚本 (Windows 版本)
仅生成 Python 消息类
"""
import os
import sys
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    proto_dir = project_root / "proto"
    output_dir = project_root / "app" / "proto"
    
    print("=" * 50)
    print("Protocol Buffers 代码生成")
    print("=" * 50)
    print()
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 __init__.py
    (output_dir / "__init__.py").touch()
    
    # 查找所有 proto 文件
    proto_files = list(proto_dir.glob("*.proto"))
    
    if not proto_files:
        print(f"警告：在 {proto_dir} 中未找到 .proto 文件")
        return 0
    
    print(f"找到 {len(proto_files)} 个 proto 文件")
    for pf in proto_files:
        print(f" - {pf.name}")
    print()
    
    # 使用 protoc 生成 Python 代码
    try:
        from grpc_tools import protoc
        
        for proto_file in proto_files:
            filename = proto_file.name
            print(f"处理：{filename}")
            
            # 构建参数列表 - 仅生成 Python 代码
            args = [
                '',
                f'-I{proto_dir}',
                f'--python_out={output_dir}',
                str(proto_file)
            ]
            result = protoc.main(args)
            
            if result == 0:
                print(f"  ✓ 生成成功")
            else:
                print(f"  ✗ 生成失败")
                return 1
        
        print()
        print("=" * 50)
        print("代码生成完成!")
        print("=" * 50)
        print()
        
        # 显示生成的文件
        print("生成的文件:")
        py_files = sorted(output_dir.glob("*_pb2.py"))
        for f in py_files:
            print(f" - {f.name}")
        print()
        print("提示:")
        print(" - .py 文件是生成的 Python 消息类")
        print(" - 可以在代码中导入使用，例如：from app.proto import demo_pb2")
        print()
        
        return 0
        
    except ImportError:
        print("错误：grpc_tools 未安装")
        print("请运行：pip install grpcio-tools")
        return 1
    except Exception as e:
        print(f"错误：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
