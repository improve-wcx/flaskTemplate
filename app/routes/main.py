"""
Main routes - homepage, favicon, etc.
"""
from flask import Blueprint, current_app, g, render_template
from utils.logger import get_request_id

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页 - 静态资源展示页"""
    request_id = get_request_id()
    current_app.logger.info("Handling index route", extra={'request_id': request_id})
    return render_template('index.html')


@main_bp.route('/hello')
def hello():
    """Hello World 路由 - 用于演示和测试"""
    request_id = get_request_id()
    current_app.logger.info("Handling hello route", extra={'request_id': request_id})
    return "Hello, World!"


@main_bp.route('/demo')
def demo():
    """演示页面 - 静态资源演示"""
    request_id = get_request_id()
    current_app.logger.info("Handling demo route", extra={'request_id': request_id})
    return render_template('static_demo.html')


@main_bp.route('/favicon.ico')
def favicon():
    """Favicon route - returns 204 No Content."""
    request_id = get_request_id()
    current_app.logger.info("Handling favicon route", extra={'request_id': request_id})
    return "", 204
