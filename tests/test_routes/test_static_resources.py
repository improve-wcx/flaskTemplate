"""
静态资源路由测试
"""
import pytest
from flask import url_for


class TestStaticResources:
    """静态资源路由测试类"""
    
    def test_main_index_page(self, client):
        """测试主首页（现在由 main_bp 处理）"""
        response = client.get('/')
        assert response.status_code == 200
        response_text = response.data.decode('utf-8')
        assert 'Flask Application' in response_text
        assert '首页' in response_text
    
    # The demo page has been removed; ensure the route returns 404.
    def test_main_demo_page_not_found(self, client):
        """确保已删除的演示页面返回 404"""
        response = client.get('/demo')
        assert response.status_code == 404
    
    def test_static_bp_index_page(self, client):
        """测试备用静态资源首页（/resources/）"""
        response = client.get('/resources/')
        assert response.status_code == 200
        # The demo page has been removed; template inheritance and block tests that relied on it are no longer applicable.
        """测试 JavaScript 文件访问"""
        response = client.get('/static/js/main.js')
        assert response.status_code == 200
        assert response.content_type.startswith('application/javascript')
        assert b'Flask Application' in response.data
        assert b'showMessage' in response.data
    
    def test_static_image_file(self, client):
        """测试图片文件访问"""
        response = client.get('/static/images/logo.svg')
        assert response.status_code == 200
        assert response.content_type.startswith('image/svg+xml')
        assert b'<svg' in response.data
    
    def test_static_audio_readme(self, client):
        """测试音频目录 README"""
        response = client.get('/static/audio/README.md')
        assert response.status_code == 200
        response_text = response.data.decode('utf-8')
        assert '音频文件' in response_text or 'Audio' in response_text
    
    # Since the demo page is removed, template inheritance tests that relied on it are no longer applicable.
    
    def test_static_file_404(self, client):
        """测试不存在的静态文件返回 404"""
        response = client.get('/static/css/nonexistent.css')
        assert response.status_code == 404
    
    def test_static_page_navigation(self, client):
        """测试静态页面导航链接"""
        response = client.get('/')
        assert response.status_code == 200
        # 检查是否包含导航链接
        assert b'/api/apis' in response.data or b'API' in response.data


class TestStaticAssets:
    """静态资源功能测试"""
    
    def test_css_loading(self, client):
        """测试 CSS 正确加载"""
        response = client.get('/static/css/main.css')
        assert response.status_code == 200
        # 检查关键 CSS 类
        assert b'.container' in response.data
        assert b'.navbar' in response.data
        assert b'.btn' in response.data
    
    def test_js_loading(self, client):
        """测试 JavaScript 正确加载"""
        response = client.get('/static/js/main.js')
        assert response.status_code == 200
        # 检查关键函数
        assert b'showMessage' in response.data
        assert b'ajaxRequest' in response.data
        assert b'DOMContentLoaded' in response.data
    
    def test_image_format(self, client):
        """测试图片格式正确"""
        response = client.get('/static/images/logo.svg')
        assert response.status_code == 200
        assert b'<svg' in response.data
        assert b'</svg>' in response.data
