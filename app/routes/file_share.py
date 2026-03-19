"""
文件共享路由模块
"""
import os
import shutil
from flask import Blueprint, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from app.utils.helpers import get_safe_path, BASE_UPLOAD_DIR

file_share_bp = Blueprint('file_share', __name__)


@file_share_bp.route('/share_files')
def share_files():
    """文件共享管理页面"""
    return render_template('share_files.html')


@file_share_bp.route('/api/list', defaults={'req_path': ''}, methods=['GET'])
@file_share_bp.route('/api/list/<path:req_path>', methods=['GET'])
def list_directory(req_path):
    """获取目录下的文件和文件夹列表"""
    abs_path = get_safe_path(req_path)
    
    if not abs_path or not os.path.exists(abs_path) or not os.path.isdir(abs_path):
        return jsonify({'error': '目录不存在或无权访问'}), 404
    
    items = []
    for item_name in os.listdir(abs_path):
        item_path = os.path.join(abs_path, item_name)
        is_dir = os.path.isdir(item_path)
        items.append({
            'name': item_name,
            'is_dir': is_dir,
            # 如果是文件，返回文件大小；如果是目录，返回空
            'size': os.path.getsize(item_path) if not is_dir else None
        })
    
    # 排序：让文件夹排在前面，文件排在后面，且按字母顺序
    items.sort(key=lambda x: (not x['is_dir'], x['name']))
    
    return jsonify({
        'current_path': req_path,
        'items': items
    }), 200


@file_share_bp.route('/api/mkdir', methods=['POST'])
def make_directory():
    """新建文件夹"""
    data = request.json
    req_path = data.get('path', '')
    folder_name = secure_filename(data.get('folder_name', ''))
    
    if not folder_name:
        return jsonify({'error': '文件夹名称不能为空或包含非法字符'}), 400
    
    abs_path = get_safe_path(os.path.join(req_path, folder_name))
    if not abs_path:
        return jsonify({'error': '非法路径'}), 403
    
    if os.path.exists(abs_path):
        return jsonify({'error': '同名文件或文件夹已存在'}), 400
    
    os.makedirs(abs_path)
    return jsonify({'message': '文件夹创建成功'}), 200


@file_share_bp.route('/api/upload', defaults={'req_path': ''}, methods=['POST'])
@file_share_bp.route('/api/upload/<path:req_path>', methods=['POST'])
def upload_file(req_path):
    """上传文件到指定层级目录"""
    abs_path = get_safe_path(req_path)
    
    if not abs_path or not os.path.isdir(abs_path):
        return jsonify({'error': '目标目录不存在'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(abs_path, filename)
        file.save(save_path)
        return jsonify({'message': '上传成功', 'filename': filename}), 200


@file_share_bp.route('/api/download/<path:req_path>', methods=['GET'])
def download_file(req_path):
    """下载指定层级的文件"""
    abs_path = get_safe_path(req_path)
    
    if not abs_path or not os.path.isfile(abs_path):
        return jsonify({'error': '文件不存在或无权访问'}), 404
    
    # 分离出目录路径和文件名，供 send_from_directory 使用
    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)
    return send_from_directory(directory, filename, as_attachment=True)


@file_share_bp.route('/api/delete/<path:req_path>', methods=['DELETE'])
def delete_item(req_path):
    """删除文件或文件夹"""
    abs_path = get_safe_path(req_path)
    
    # 核心防御：绝对不允许删除基础上传目录
    if not abs_path or abs_path == BASE_UPLOAD_DIR:
        return jsonify({'error': '非法操作：不能删除根目录'}), 403
    
    if not os.path.exists(abs_path):
        return jsonify({'error': '目标不存在'}), 404
    
    try:
        if os.path.isfile(abs_path):
            os.remove(abs_path)  # 删除文件
        else:
            shutil.rmtree(abs_path)  # 递归删除整个文件夹及其内容
        
        return jsonify({'message': '删除成功'}), 200
    except Exception as e:
        return jsonify({'error': f'删除失败：{str(e)}'}), 500
