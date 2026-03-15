#!/usr/bin/env python3
"""
命令行客户端 - 用于调用所有 Web API 接口

支持所有通过 Web API 实现的功能，提供命令行界面。
使用 --help 查看可用命令和参数说明。

示例:
    # 健康检查
    python -m cli health
    
    # 获取版本信息
    python -m cli version
    
    # 问候（GET）
    python -m cli hello --get
    
    # 问候（POST）
    python -m cli hello --post --name "Alice"
    
    # 获取用户信息
    python -m cli user 12345
    
    # 获取用户列表
    python -m cli users --page 1 --page-size 10
    
    # Echo 测试
    python -m cli echo --data '{"key": "value"}'
    
    # 查看所有命令
    python -m cli --help
    
    # 查看特定命令帮助
    python -m cli hello --help
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from urllib.parse import urlencode


# 默认配置
DEFAULT_BASE_URL = "http://127.0.0.1:5000"


def make_request(url, method="GET", data=None, headers=None):
    """
    发送 HTTP 请求
    
    Args:
        url: 请求 URL
        method: HTTP 方法 (GET, POST, PUT, DELETE)
        data: 请求数据 (字典或 JSON 字符串)
        headers: 请求头
    
    Returns:
        tuple: (status_code, response_data)
    """
    if headers is None:
        headers = {}
    
    if data and isinstance(data, dict):
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    elif data and isinstance(data, str):
        data = data.encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = response.read().decode('utf-8')
            return response.status, json.loads(response_data) if response_data else {}
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        return e.code, json.loads(error_data) if error_data else {"error": str(e)}
    except urllib.error.URLError as e:
        return None, {"error": f"无法连接到服务器：{e.reason}"}
    except Exception as e:
        return None, {"error": f"请求失败：{str(e)}"}


def print_response(status_code, data, pretty=True):
    """打印响应结果"""
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))
    
    if status_code and status_code >= 400:
        return 1
    return 0


# ========== 命令实现 ==========

def cmd_health(args):
    """健康检查"""
    url = f"{args.base_url}/api/health"
    status_code, data = make_request(url)
    print(f"URL: {url}")
    print(f"状态码：{status_code}")
    print("-" * 50)
    return print_response(status_code, data)


def cmd_version(args):
    """版本信息"""
    url = f"{args.base_url}/api/version"
    status_code, data = make_request(url)
    print(f"URL: {url}")
    print(f"状态码：{status_code}")
    print("-" * 50)
    return print_response(status_code, data)


def cmd_hello(args):
    """问候接口"""
    if args.get:
        # GET 请求
        url = f"{args.base_url}/api/v1/demo/hello"
        print(f"URL: {url}")
        print(f"方法：GET")
        print("-" * 50)
        status_code, data = make_request(url)
        return print_response(status_code, data)
    
    elif args.post:
        # POST 请求
        url = f"{args.base_url}/api/v1/demo/hello"
        data = {}
        if args.name:
            data['name'] = args.name
        
        print(f"URL: {url}")
        print(f"方法：POST")
        print(f"请求数据：{data}")
        print("-" * 50)
        status_code, response_data = make_request(url, method="POST", data=data)
        return print_response(status_code, response_data)
    
    else:
        print("错误：必须指定 --get 或 --post")
        return 1


def cmd_user(args):
    """获取用户信息"""
    url = f"{args.base_url}/api/v1/demo/user/{args.user_id}"
    print(f"URL: {url}")
    print(f"方法：GET")
    print("-" * 50)
    status_code, data = make_request(url)
    return print_response(status_code, data)


def cmd_users(args):
    """获取用户列表"""
    url = f"{args.base_url}/api/v1/demo/users"
    data = {
        'page': args.page,
        'page_size': args.page_size
    }
    
    print(f"URL: {url}")
    print(f"方法：POST")
    print(f"请求数据：{data}")
    print("-" * 50)
    status_code, response_data = make_request(url, method="POST", data=data)
    return print_response(status_code, response_data)


def cmd_echo(args):
    """Echo 接口"""
    url = f"{args.base_url}/api/v1/demo/echo"
    
    # 解析数据
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            print(f"错误：无效的 JSON 数据：{args.data}")
            return 1
    else:
        data = {}
    
    print(f"URL: {url}")
    print(f"方法：POST")
    print(f"请求数据：{data}")
    print("-" * 50)
    status_code, response_data = make_request(url, method="POST", data=data)
    return print_response(status_code, response_data)


def cmd_admin(args):
    """管理后台（仅信息）"""
    url = f"{args.base_url}/admin/"
    print(f"URL: {url}")
    print(f"方法：GET")
    print("-" * 50)
    print("注意：管理后台尚未实现完整功能")
    return 0


def cmd_home(args):
    """首页"""
    url = f"{args.base_url}/"
    print(f"URL: {url}")
    print(f"方法：GET")
    print("-" * 50)
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            print(f"状态码：{response.status}")
            print(f"内容：{content}")
            return 0
    except Exception as e:
        print(f"错误：{str(e)}")
        return 1


def cmd_apis(args):
    """查询所有可用接口"""
    url = f"{args.base_url}/api/apis"
    print(f"URL: {url}")
    print(f"方法：GET")
    print("-" * 50)
    status_code, data = make_request(url)
    return print_response(status_code, data)


# ========== 主函数 ==========

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog='cli',
        description='Web API 命令行客户端 - 调用所有 Web API 接口',
        epilog='示例:\n'
               '  python -m cli health\n'
               '  python -m cli hello --post --name "Alice"\n'
               '  python -m cli user 12345\n'
               '  python -m cli users --page 1 --page-size 10\n'
               '  python -m cli echo --data \'{"key": "value"}\'\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--base-url', '-b',
        default=DEFAULT_BASE_URL,
        help=f'API 基础 URL (默认：{DEFAULT_BASE_URL})'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # health 命令
    health_parser = subparsers.add_parser('health', help='健康检查')
    health_parser.set_defaults(func=cmd_health)
    
    # version 命令
    version_parser = subparsers.add_parser('version', help='版本信息')
    version_parser.set_defaults(func=cmd_version)
    
    # hello 命令
    hello_parser = subparsers.add_parser('hello', help='问候接口')
    hello_group = hello_parser.add_mutually_exclusive_group(required=True)
    hello_group.add_argument('--get', action='store_true', help='使用 GET 方法')
    hello_group.add_argument('--post', action='store_true', help='使用 POST 方法')
    hello_parser.add_argument('--name', '-n', help='姓名（仅 POST 有效）')
    hello_parser.set_defaults(func=cmd_hello)
    
    # user 命令
    user_parser = subparsers.add_parser('user', help='获取用户信息')
    user_parser.add_argument('user_id', help='用户 ID')
    user_parser.set_defaults(func=cmd_user)
    
    # users 命令
    users_parser = subparsers.add_parser('users', help='获取用户列表')
    users_parser.add_argument('--page', '-p', type=int, default=1, help='页码 (默认：1)')
    users_parser.add_argument('--page-size', '-s', type=int, default=10, help='每页数量 (默认：10)')
    users_parser.set_defaults(func=cmd_users)
    
    # echo 命令
    echo_parser = subparsers.add_parser('echo', help='Echo 接口')
    echo_parser.add_argument('--data', '-d', help='JSON 数据')
    echo_parser.set_defaults(func=cmd_echo)
    
    # admin 命令
    admin_parser = subparsers.add_parser('admin', help='管理后台')
    admin_parser.set_defaults(func=cmd_admin)
    
    # home 命令
    home_parser = subparsers.add_parser('home', help='首页')
    home_parser.set_defaults(func=cmd_home)
    
    # apis 命令
    apis_parser = subparsers.add_parser('apis', help='查询所有可用接口')
    apis_parser.set_defaults(func=cmd_apis)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
