"""
HEIGO 足球经理联赛管理系统 - Railway 生产版
使用 Gunicorn 生产服务器
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取端口
PORT = int(os.environ.get('PORT', 5000))

# 创建应用
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'heigo-secret-2024')

# 数据库配置 - 使用绝对路径
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heigo_league.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==================== 数据模型 ====================

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coach_name = db.Column(db.String(100))
    league_level = db.Column(db.String(20), default='甲级')
    played = db.Column(db.Integer, default=0)
    won = db.Column(db.Integer, default=0)
    drawn = db.Column(db.Integer, default=0)
    lost = db.Column(db.Integer, default=0)
    goals_for = db.Column(db.Integer, default=0)
    goals_against = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'coach_name': self.coach_name,
            'league_level': self.league_level, 'played': self.played,
            'won': self.won, 'drawn': self.drawn, 'lost': self.lost,
            'goals_for': self.goals_for, 'goals_against': self.goals_against,
            'goal_difference': self.goals_for - self.goals_against,
            'points': self.points
        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    match_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    
    def to_dict(self):
        return {
            'id': self.id, 'round': self.round,
            'home_team': self.home_team, 'away_team': self.away_team,
            'home_score': self.home_score, 'away_score': self.away_score,
            'match_date': self.match_date, 'status': self.status
        }


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    from_team = db.Column(db.String(100))
    to_team = db.Column(db.String(100))
    transfer_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id, 'player_name': self.player_name,
            'from_team': self.from_team, 'to_team': self.to_team,
            'transfer_type': self.transfer_type, 'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }


class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(100), nullable=False)
    club_name = db.Column(db.String(200), nullable=False)
    league_level = db.Column(db.String(20), default='甲级')
    rating = db.Column(db.String(1), default='C')
    stars = db.Column(db.Integer, default=1)
    honors = db.Column(db.Text, default='')
    join_date = db.Column(db.String(50))
    
    @property
    def honor_count(self):
        return len([h for h in self.honors.split(',') if h.strip()]) if self.honors else 0
    
    def to_dict(self):
        return {
            'id': self.id, 'game_id': self.game_id, 'club_name': self.club_name,
            'league_level': self.league_level, 'rating': self.rating,
            'stars': self.stars, 'honors': self.honors,
            'honor_count': self.honor_count, 'join_date': self.join_date
        }


# ==================== 路由 ====================

@app.route('/')
def index():
    logger.info('Serving index.html')
    return send_from_directory('.', 'index.html')


@app.route('/health')
def health():
    """健康检查 - Railway 会访问这个端点"""
    logger.info(f'Health check requested on port {PORT}')
    return jsonify({
        'status': 'healthy',
        'port': PORT,
        'database': 'connected'
    }), 200


@app.route('/ready')
def ready():
    """就绪检查"""
    try:
        Team.query.first()
        return jsonify({'ready': True}), 200
    except Exception as e:
        logger.error(f'Readiness check failed: {e}')
        return jsonify({'ready': False, 'error': str(e)}), 500


@app.route('/api/standings')
def get_standings():
    level = request.args.get('level', '甲级')
    teams = Team.query.filter_by(league_level=level).all()
    teams = sorted(teams, key=lambda t: (t.points, t.goals_for - t.goals_against, t.goals_for), reverse=True)
    return jsonify([t.to_dict() for t in teams])


@app.route('/api/teams')
def get_teams():
    teams = Team.query.all()
    return jsonify([t.to_dict() for t in teams])


@app.route('/api/matches', methods=['GET', 'POST'])
def matches():
    if request.method == 'POST':
        data = request.get_json()
        match = Match(
            round=data.get('round', 1),
            home_team=data.get('home_team'),
            away_team=data.get('away_team'),
            home_score=data.get('home_score', 0),
            away_score=data.get('away_score', 0),
            match_date=data.get('match_date'),
            status='finished'
        )
        db.session.add(match)
        update_standings(match)
        db.session.commit()
        return jsonify({'success': True})
    
    matches = Match.query.order_by(Match.round).all()
    return jsonify([m.to_dict() for m in matches])


def update_standings(match):
    home = Team.query.filter_by(name=match.home_team).first()
    away = Team.query.filter_by(name=match.away_team).first()
    if not home or not away:
        return
    
    home.played += 1
    away.played += 1
    home.goals_for += match.home_score
    home.goals_against += match.away_score
    away.goals_for += match.away_score
    away.goals_against += match.home_score
    
    if match.home_score > match.away_score:
        home.won += 1
        home.points += 3
        away.lost += 1
    elif match.home_score < match.away_score:
        away.won += 1
        away.points += 3
        home.lost += 1
    else:
        home.drawn += 1
        away.drawn += 1
        home.points += 1
        away.points += 1


@app.route('/api/transfers', methods=['GET', 'POST'])
def transfers():
    if request.method == 'POST':
        data = request.get_json()
        transfer = Transfer(
            player_name=data.get('player_name'),
            from_team=data.get('from_team'),
            to_team=data.get('to_team'),
            transfer_type=data.get('transfer_type'),
            status='pending'
        )
        db.session.add(transfer)
        db.session.commit()
        return jsonify({'success': True})
    
    transfers = Transfer.query.order_by(Transfer.created_at.desc()).all()
    return jsonify([t.to_dict() for t in transfers])


@app.route('/api/coaches')
def get_coaches():
    coaches = Coach.query.all()
    return jsonify([c.to_dict() for c in coaches])


@app.route('/api/stats')
def get_stats():
    return jsonify({
        'total_teams': Team.query.count(),
        'total_matches': Match.query.count(),
        'total_coaches': Coach.query.count()
    })


# ==================== 初始化 ====================

def init_db():
    """初始化数据库"""
    logger.info('Initializing database...')
    with app.app_context():
        db.create_all()
        
        if Team.query.count() == 0:
            logger.info('Creating sample data...')
            teams = [
                Team(name='托特纳姆热刺', coach_name='MagicChicken', league_level='超级'),
                Team(name='拜仁慕尼黑', coach_name='CoachWang', league_level='甲级'),
                Team(name='AC 米兰', coach_name='ItalianCoach', league_level='甲级'),
                Team(name='利物浦', coach_name='KlopFan', league_level='超级'),
            ]
            db.session.add_all(teams)
            
            coaches = [
                Coach(game_id='MagicChicken', club_name='托特纳姆热刺', league_level='超级', rating='S', stars=5),
                Coach(game_id='CoachWang', club_name='拜仁慕尼黑', league_level='甲级', rating='A', stars=3),
            ]
            db.session.add_all(coaches)
            db.session.commit()
            logger.info('✅ Sample data created')
        else:
            logger.info(f'Database already initialized with {Team.query.count()} teams')


# ==================== 生产环境入口 ====================

def create_app():
    """应用工厂函数 - Gunicorn 使用"""
    init_db()
    logger.info(f'HEIGO League System starting on port {PORT}')
    return app


if __name__ == '__main__':
    # 本地开发使用
    init_db()
    logger.info(f'🚀 HEIGO 联赛管理系统启动中...')
    logger.info(f'🌐 访问地址：http://0.0.0.0:{PORT}')
    logger.info(f'🔍 健康检查：http://0.0.0.0:{PORT}/health')
    
    # 生产环境配置
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
