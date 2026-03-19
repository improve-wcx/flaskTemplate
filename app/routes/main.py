"""
主页面路由
"""
import os
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页，显示所有可用工具的导航卡片"""
    tools = [
        {
            "title": "番茄闹钟",
            "description": "专注时钟，助力高效工作与学习。",
            "icon": "bi-alarm",
            "url": "/timer",
            "color": "text-danger"
        },
        {
            "title": "文件共享",
            "description": "局域网文件快速传输与管理。",
            "icon": "bi-folder2-open",
            "url": "/share_files",
            "color": "text-primary"
        },
        {
            "title": "文本共享",
            "description": "跨设备剪贴板，实时同步文本内容。",
            "icon": "bi-clipboard-data",
            "url": "/text-share",
            "color": "text-success"
        }
    ]
    return render_template('index.html', tools=tools)


@main_bp.route('/favicon.ico')
def serve_favicon():
    """返回网站图标"""
    from flask import send_from_directory
    from app.config import project_root
    
    return send_from_directory(
        os.path.join(project_root, 'static', 'image'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@main_bp.route('/hello1')
def hello():
    """测试路由"""
    return 'Hello, World!'


@main_bp.route('/timer')
def timer():
    """番茄钟计时器页面"""
    return render_template('web_timer.html')
