"""
静态资源相关路由
提供 HTML 页面和静态资源访问
"""

from flask import Blueprint, render_template
from app.api_registry import register_api

# 保留 static_bp 用于管理静态资源相关页面（如果需要独立分类）
static_bp = Blueprint("static_bp", __name__, url_prefix="/resources")


@static_bp.route("/")
@register_api(path="/resources/", method="GET", category="静态资源", description="备用首页，渲染主页面模板")
def static_index():
    """静态资源首页（备用）"""
    return render_template("index.html")


