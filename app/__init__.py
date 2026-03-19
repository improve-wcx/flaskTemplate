"""
Flask 应用包
"""
import os
from app.config import create_app
from app.models.database import init_db

# 创建应用实例
app = create_app()

# 确保上传目录存在
os.makedirs('upload', exist_ok=True)

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(debug=True)
