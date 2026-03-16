"""
静态资源相关路由
提供 HTML 页面和静态资源访问
"""
from flask import Blueprint, render_template, send_from_directory, current_app
import os

static_bp = Blueprint('static_bp', __name__, url_prefix='/static-pages')


@static_bp.route('/')
def static_index():
    """静态资源首页"""
    return render_template('index.html')


@static_bp.route('/demo')
def static_demo():
    """静态资源演示页面"""
    return render_template('static_demo.html')
