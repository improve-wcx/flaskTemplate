"""
Main routes - homepage, favicon, etc.
"""

from flask import Blueprint, current_app, render_template

from utils.logger import get_request_id
from app.api_registry import register_api

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@register_api(path="/", method="GET", category="系统", description="首页入口，渲染首页模板")
def index():
    """首页 - 静态资源展示页"""
    request_id = get_request_id()
    current_app.logger.info("Handling index route", extra={"request_id": request_id})
    return render_template("index.html")


@main_bp.route("/hello")
@register_api(path="/hello", method="GET", category="系统", description="返回 Hello World 示例文字")
def hello():
    """Hello World 路由 - 用于演示和测试"""
    request_id = get_request_id()
    current_app.logger.info("Handling hello route", extra={"request_id": request_id})
    return "Hello, World!"




@main_bp.route("/favicon.ico")
@register_api(path="/favicon.ico", method="GET", category="系统", description="返回 204，提供 favicon 占位")
def favicon():
    """Favicon route - returns 204 No Content."""
    request_id = get_request_id()
    current_app.logger.info("Handling favicon route", extra={"request_id": request_id})
    return "", 204
