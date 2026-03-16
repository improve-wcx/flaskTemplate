"""关系图页面路由"""

import os

from flask import Blueprint, send_from_directory

rel_map_bp = Blueprint("rel_map", __name__)


@rel_map_bp.route("/relationship-map")
@rel_map_bp.route("/relationship-map/")
def relationship_map():
    """直接返回静态 HTML 文件"""
    # 获取当前文件所在目录的上级目录（即项目根目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))  # app/routes
    project_root = os.path.dirname(current_dir)  # app
    static_html_dir = os.path.join(project_root, "static", "html")  # app/static/html
    return send_from_directory(static_html_dir, "releationships_map.html")
