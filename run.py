"""
HEIGO 足球经理联赛管理系统 - Railway 部署版本
"""
import os
from app import create_app

# 创建 Flask 应用
app = create_app()

# Railway 使用 PORT 环境变量
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting HEIGO League System on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
