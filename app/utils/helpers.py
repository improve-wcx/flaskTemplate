"""
工具函数模块
"""
import os
from werkzeug.utils import secure_filename

# 基础配置
BASE_UPLOAD_DIR = os.path.abspath('upload')

# 定义音频根目录
AUDIO_ROOT = os.path.join('static', 'audio')


def get_safe_path(subpath, base_dir=None):
    """
    核心安全函数：防止目录遍历攻击 (Path Traversal)
    
    无论用户传入什么乱七八糟的路径 (比如 ../../../etc/passwd)
    该函数都会将其限制在 base_dir 内部。
    
    Args:
        subpath: 用户输入的路径
        base_dir: 基础目录，默认为 BASE_UPLOAD_DIR
    
    Returns:
        安全的路径，如果路径不安全则返回 None
    """
    if base_dir is None:
        base_dir = BASE_UPLOAD_DIR
        
    if not subpath:
        subpath = ''
    
    # 规范化路径，去掉多余的斜杠
    safe_subpath = os.path.normpath(subpath).lstrip(os.sep)
    
    # 拼接出绝对路径
    target_path = os.path.abspath(os.path.join(base_dir, safe_subpath))
    
    # 安全校验：确保最终的绝对路径仍然在基础目录内
    if not target_path.startswith(base_dir):
        return None
    
    return target_path
