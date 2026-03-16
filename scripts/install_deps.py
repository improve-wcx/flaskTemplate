#!/usr/bin/env python3
"""
自动检测平台并安装对应依赖的脚本
"""
import sys
import subprocess
import platform

def get_platform():
    """检测当前操作系统"""
    system = platform.system().lower()
    if system == 'linux':
        return 'linux'
    elif system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    else:
        return 'unknown'

def get_python_version():
    """获取 Python 版本"""
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def main():
    current_platform = get_platform()
    python_version = get_python_version()
    
    print("=" * 60)
    print("Flask 项目依赖安装向导")
    print("=" * 60)
    print(f"检测到平台：{current_platform.upper()}")
    print(f"Python 版本：{python_version}")
    print()
    
    if current_platform == 'unknown':
        print("警告：无法识别的操作系统，使用基础依赖")
        requirements_file = 'requirements/base.txt'
    else:
        requirements_file = f'requirements/{current_platform}.txt'
    
    print(f"推荐安装文件：{requirements_file}")
    print()
    
    # 询问用户
    response = input("是否继续安装？(Y/n): ").strip().lower()
    if response in ['', 'y', 'yes']:
        print(f"\n正在安装依赖：{requirements_file}...")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                check=True
            )
            print("-" * 60)
            print("✓ 依赖安装成功!")
            print()
            print("下一步:")
            if current_platform == 'windows':
                print("  1. 生成 Protobuf 代码：python scripts/generate_protobuf_win.py")
            else:
                print("  1. 生成 Protobuf 代码：python scripts/generate_protobuf.py")
            print("  2. 运行测试：pytest tests/ -v")
            print("  3. 启动服务：python run.py")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"✗ 依赖安装失败：{e}")
            return 1
        except FileNotFoundError:
            print("✗ pip 未找到，请确保 Python 已正确安装")
            return 1
    else:
        print("已取消安装")
        print()
        print("手动安装命令:")
        print(f"  pip install -r {requirements_file}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
