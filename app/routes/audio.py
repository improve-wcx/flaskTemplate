"""
音频播放路由模块
"""
import os
from flask import Blueprint, jsonify, render_template
from app.utils.helpers import AUDIO_ROOT

audio_bp = Blueprint('audio', __name__)


@audio_bp.route('/ogg_audio')
def ogg_audio():
    """渲染音频播放器主页"""
    return render_template('ogg_audio.html')


@audio_bp.route('/api/get_audio_list')
def get_audio_list():
    """
    深度扫描 AUDIO_ROOT 及其所有子目录下的 ogg 文件
    返回格式：[{"name": "animals/lion.ogg", "path": "animals/lion.ogg"}, ...]
    """
    audio_files = []
    
    try:
        # 如果根目录不存在则直接返回空
        if not os.path.exists(AUDIO_ROOT):
            return jsonify({"success": True, "files": []})
        
        # os.walk 会递归遍历所有子目录
        for root, dirs, files in os.walk(AUDIO_ROOT):
            for file in files:
                if file.lower().endswith('.ogg'):
                    # 获取文件相对于 AUDIO_ROOT 的路径
                    # 例如：static/audio/animals/lion.ogg -> animals/lion.ogg
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, AUDIO_ROOT)
                    
                    # 将路径分隔符统一转换为正斜杠 /，防止 Windows 系统的反斜杠 \ 导致前端加载失败
                    web_path = rel_path.replace(os.sep, '/')
                    
                    audio_files.append({
                        "display_name": web_path,  # 用于下拉框显示
                        "file_path": web_path  # 用于拼接 URL
                    })
        
        # 按照名称排序
        audio_files.sort(key=lambda x: x['display_name'])
        
        return jsonify({
            "success": True,
            "files": audio_files,
            "count": len(audio_files)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
