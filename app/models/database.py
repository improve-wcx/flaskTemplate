"""
数据库相关配置和工具函数
"""
import sqlite3

DB_FILE = 'text_share.db'


def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建文本存储表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shared_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 将查询结果转换为字典
    return conn
