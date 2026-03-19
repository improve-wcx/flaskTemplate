"""
应用配置和初始化
"""
import os
from flask import Flask

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    """应用工厂函数"""
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, 'templates'),
        static_folder=os.path.join(project_root, 'static')
    )
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.text_share import text_share_bp
    from app.routes.file_share import file_share_bp
    from app.routes.audio import audio_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(text_share_bp)
    app.register_blueprint(file_share_bp)
    app.register_blueprint(audio_bp)
    
    return app
