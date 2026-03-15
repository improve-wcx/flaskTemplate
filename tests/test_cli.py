"""命令行客户端单元测试"""
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import (
    make_request,
    print_response,
    cmd_health,
    cmd_version,
    cmd_hello,
    cmd_user,
    cmd_users,
    cmd_echo,
    cmd_admin,
    cmd_home,
    DEFAULT_BASE_URL
)


class TestMakeRequest(unittest.TestCase):
    """测试 make_request 函数"""

    def test_url_error(self):
        """测试 URL 错误"""
        status_code, data = make_request('http://nonexistent.invalid.domain:9999/api')

        self.assertIsNone(status_code)
        self.assertIn('无法连接到服务器', data['error'])


class TestPrintResponse(unittest.TestCase):
    """测试 print_response 函数"""

    @patch('cli.print')
    def test_success_response(self, mock_print):
        """测试成功响应"""
        result = print_response(200, {'status': 'ok'}, pretty=False)
        self.assertEqual(result, 0)

    @patch('cli.print')
    def test_error_response(self, mock_print):
        """测试错误响应"""
        result = print_response(404, {'error': 'not found'}, pretty=False)
        self.assertEqual(result, 1)


class TestCmdHealth(unittest.TestCase):
    """测试 health 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_health_success(self, mock_print, mock_make_request):
        """测试健康检查成功"""
        mock_make_request.return_value = (200, {'status': 'healthy'})

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL

        result = cmd_health(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()


class TestCmdVersion(unittest.TestCase):
    """测试 version 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_version_success(self, mock_print, mock_make_request):
        """测试版本查询成功"""
        mock_make_request.return_value = (200, {'version': '1.0.0'})

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL

        result = cmd_version(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()


class TestCmdHello(unittest.TestCase):
    """测试 hello 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_hello_get(self, mock_print, mock_make_request):
        """测试 GET 问候"""
        mock_make_request.return_value = (200, {'message': 'Hello, World!'})

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.get = True
        args.post = False
        args.name = None

        result = cmd_hello(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()

    @patch('cli.make_request')
    @patch('cli.print')
    def test_hello_post_with_name(self, mock_print, mock_make_request):
        """测试 POST 问候（带姓名）"""
        mock_make_request.return_value = (200, {'message': 'Hello, Alice!'})

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.get = False
        args.post = True
        args.name = 'Alice'

        result = cmd_hello(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()

    @patch('cli.print')
    def test_hello_no_method(self, mock_print):
        """测试未指定方法"""
        args = MagicMock()
        args.get = False
        args.post = False

        result = cmd_hello(args)

        self.assertEqual(result, 1)


class TestCmdUser(unittest.TestCase):
    """测试 user 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_user_found(self, mock_print, mock_make_request):
        """测试用户存在"""
        mock_make_request.return_value = (200, {
            'success': True,
            'user': {'user_id': '12345'}
        })

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.user_id = '12345'

        result = cmd_user(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()

    @patch('cli.make_request')
    @patch('cli.print')
    def test_user_not_found(self, mock_print, mock_make_request):
        """测试用户不存在"""
        mock_make_request.return_value = (404, {
            'success': False,
            'message': 'User not found'
        })

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.user_id = '99999'

        result = cmd_user(args)

        self.assertEqual(result, 1)


class TestCmdUsers(unittest.TestCase):
    """测试 users 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_users_list(self, mock_print, mock_make_request):
        """测试用户列表"""
        mock_make_request.return_value = (200, {
            'success': True,
            'users': [],
            'total': 100,
            'page': 1,
            'pageSize': 10
        })

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.page = 1
        args.page_size = 10

        result = cmd_users(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()


class TestCmdEcho(unittest.TestCase):
    """测试 echo 命令"""

    @patch('cli.make_request')
    @patch('cli.print')
    def test_echo_with_data(self, mock_print, mock_make_request):
        """测试 Echo 带数据"""
        mock_make_request.return_value = (200, {
            'statusCode': 0,
            'echo_data': {'key': 'value'}
        })

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL
        args.data = '{"key": "value"}'

        result = cmd_echo(args)

        self.assertEqual(result, 0)
        mock_make_request.assert_called_once()

    @patch('cli.print')
    def test_echo_invalid_json(self, mock_print):
        """测试 Echo 无效 JSON"""
        args = MagicMock()
        args.data = 'invalid json'

        result = cmd_echo(args)

        self.assertEqual(result, 1)


class TestCmdAdmin(unittest.TestCase):
    """测试 admin 命令"""

    @patch('cli.print')
    def test_admin(self, mock_print):
        """测试管理后台"""
        args = MagicMock()

        result = cmd_admin(args)

        self.assertEqual(result, 0)


class TestCmdHome(unittest.TestCase):
    """测试 home 命令"""

    @patch('cli.urllib.request.urlopen')
    @patch('cli.print')
    def test_home_success(self, mock_print, mock_urlopen):
        """测试首页成功"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'Hello, World!'
        mock_urlopen.return_value = mock_response

        args = MagicMock()
        args.base_url = DEFAULT_BASE_URL

        result = cmd_home(args)

        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
