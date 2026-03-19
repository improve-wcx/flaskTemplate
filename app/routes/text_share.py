"""
文本共享路由模块
"""
from flask import Blueprint, jsonify, render_template, request
from app.models.database import get_db_connection

text_share_bp = Blueprint('text_share', __name__)


@text_share_bp.route('/text-share', methods=['GET'])
def text_share_page():
    """渲染文本共享的前端页面"""
    return render_template('text_share.html')


@text_share_bp.route('/api/text-share/submit', methods=['POST'])
def submit_text():
    """接收并保存前端提交的文本"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'code': 400, 'msg': '内容不能为空'}), 400
    
    content = data['content']
    # 【关键点】：绝对不要对 content 使用 .strip() 或替换字符，原样入库以保留排版
    
    if not content:
        return jsonify({'code': 400, 'msg': '内容不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO shared_texts (content, created_at) VALUES (?, datetime("now", "localtime"))',
            (content,)
        )
        conn.commit()
        new_id = cursor.lastrowid
        
        return jsonify({
            'code': 200,
            'msg': '提交成功',
            'data': {'id': new_id}
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'服务器错误：{str(e)}'}), 500
    finally:
        conn.close()


@text_share_bp.route('/api/text-share/list', methods=['GET'])
def get_text_list():
    """获取文本列表，支持分页和搜索"""
    # 获取查询参数
    keyword = request.args.get('keyword', '').strip()
    start_time = request.args.get('start_time', '')  # 格式期望：YYYY-MM-DD HH:MM:SS
    end_time = request.args.get('end_time', '')
    
    # 分页参数
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))  # 默认每次拉取 10 条
    except ValueError:
        return jsonify({'code': 400, 'msg': '分页参数错误'}), 400
    
    offset = (page - 1) * page_size
    
    # 构建动态 SQL 查询
    query = 'SELECT * FROM shared_texts WHERE 1=1'
    params = []
    
    if keyword:
        query += ' AND content LIKE ?'
        params.append(f'%{keyword}%')
    
    if start_time:
        query += ' AND created_at >= ?'
        params.append(start_time)
    
    if end_time:
        query += ' AND created_at <= ?'
        params.append(end_time)
    
    # 按时间降序排列 (最新提交在最前)
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([page_size, offset])
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # 转换为列表字典
        data_list = [dict(row) for row in rows]
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': data_list,
            'page': page,
            'page_size': page_size,
            'has_more': len(data_list) == page_size  # 如果拉取到的数据等于 page_size，说明可能还有下一页
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'查询错误：{str(e)}'}), 500
    finally:
        conn.close()


@text_share_bp.route('/api/text-share/delete', methods=['POST'])
def delete_text():
    """根据 ID 删除指定的文本"""
    data = request.get_json()
    item_id = data.get('id')
    
    if not item_id:
        return jsonify({'code': 400, 'msg': '缺少数据 ID'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 执行删除操作
        cursor.execute('DELETE FROM shared_texts WHERE id = ?', (item_id,))
        conn.commit()
        
        # 检查是否有行被受影响（判断 ID 是否真的存在）
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'msg': '要删除的数据不存在'}), 404
        
        return jsonify({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'服务器错误：{str(e)}'}), 500
    finally:
        conn.close()
