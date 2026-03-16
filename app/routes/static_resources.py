"""
静态资源相关路由
提供 HTML 页面和静态资源访问
"""

from flask import Blueprint, render_template

# 保留 static_bp 用于管理静态资源相关页面（如果需要独立分类）
static_bp = Blueprint("static_bp", __name__, url_prefix="/resources")


@static_bp.route("/")
def static_index():
    """静态资源首页（备用）"""
    return render_template("index.html")


