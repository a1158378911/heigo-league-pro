"""
HEIGO 足球经理联赛管理系统 - 主应用
"""
import os
from flask import Flask, Blueprint, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin_login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'heigo-league-secret-2024')
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgresql://'):
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # 使用绝对路径
        instance_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{instance_dir}/heigo_league.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    from .models import Team, Match, Transfer, Coach, Announcement
    from .routes import api_bp
    from .admin_routes import admin_bp
    
    # 创建主路由 Blueprint
    main_bp = Blueprint('main_bp', __name__)
    
    @main_bp.route('/')
    def index():
        return send_from_directory(app.root_path, '../index.html')
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Admin
        return Admin.query.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        from .models import Admin
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()

    return app
