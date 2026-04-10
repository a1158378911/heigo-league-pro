"""
HEIGO 足球经理联赛管理系统 - API 路由
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models import Team, Match, Transfer, Coach, Announcement

api_bp = Blueprint('api', __name__)


# ==================== 积分榜 API ====================

@api_bp.route('/standings', methods=['GET'])
def get_standings():
    """获取积分榜"""
    level = request.args.get('level', '甲级')
    teams = Team.query.filter_by(league_level=level).all()
    
    # 按积分排序
    teams = sorted(teams, key=lambda t: (t.points, t.goal_difference, t.goals_for), reverse=True)
    
    return jsonify([team.to_dict() for team in teams])


# ==================== 球队 API ====================

@api_bp.route('/teams', methods=['GET'])
def get_teams():
    """获取球队列表"""
    level = request.args.get('level')
    search = request.args.get('search')
    
    query = Team.query
    if level:
        query = query.filter_by(league_level=level)
    if search:
        query = query.filter(Team.name.contains(search))
    
    teams = query.all()
    return jsonify([team.to_dict() for team in teams])


@api_bp.route('/teams', methods=['POST'])
@login_required
def create_team():
    """创建球队"""
    data = request.get_json()
    
    team = Team(
        name=data.get('name'),
        coach_id=data.get('coach_id'),
        league_level=data.get('league_level', '甲级')
    )
    
    db.session.add(team)
    db.session.commit()
    
    return jsonify({'success': True, 'team': team.to_dict()})


# ==================== 比赛 API ====================

@api_bp.route('/matches', methods=['GET'])
def get_matches():
    """获取比赛列表"""
    round_num = request.args.get('round')
    status = request.args.get('status')
    
    query = Match.query
    if round_num:
        query = query.filter_by(round=int(round_num))
    if status:
        query = query.filter_by(status=status)
    
    matches = query.order_by(Match.round, Match.match_date).all()
    return jsonify([match.to_dict() for match in matches])


@api_bp.route('/matches', methods=['POST'])
@login_required
def create_match():
    """录入比赛结果"""
    data = request.get_json()
    
    match = Match(
        round=data.get('round'),
        home_team_id=data.get('home_team_id'),
        away_team_id=data.get('away_team_id'),
        home_score=data.get('home_score', 0),
        away_score=data.get('away_score', 0),
        match_type=data.get('match_type', 'league')
    )
    
    db.session.add(match)
    db.session.commit()
    
    # 更新积分榜
    update_standings(match)
    
    return jsonify({'success': True, 'match': match.to_dict()})


def update_standings(match):
    """更新积分榜"""
    home = Team.query.get(match.home_team_id)
    away = Team.query.get(match.away_team_id)
    
    if not home or not away:
        return
    
    # 更新场次
    home.played += 1
    away.played += 1
    
    # 更新进球
    home.goals_for += match.home_score
    home.goals_against += match.away_score
    away.goals_for += match.away_score
    away.goals_against += match.home_score
    
    # 更新积分
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
    
    db.session.commit()


# ==================== 赛程 API ====================

@api_bp.route('/schedule', methods=['GET'])
def get_schedule():
    """获取赛程"""
    round_num = request.args.get('round')
    
    query = Match.query
    if round_num:
        query = query.filter_by(round=int(round_num))
    
    matches = query.order_by(Match.round, Match.match_date).all()
    return jsonify([match.to_dict() for match in matches])


# ==================== 交易 API ====================

@api_bp.route('/transfers', methods=['GET'])
def get_transfers():
    """获取交易记录"""
    status = request.args.get('status')
    
    query = Transfer.query
    if status:
        query = query.filter_by(status=status)
    
    transfers = query.order_by(Transfer.created_at.desc()).all()
    return jsonify([t.to_dict() for t in transfers])


@api_bp.route('/transfers', methods=['POST'])
@login_required
def create_transfer():
    """提交交易申请"""
    data = request.get_json()
    
    transfer = Transfer(
        player_name=data.get('player_name'),
        position=data.get('position'),
        from_team_id=data.get('from_team_id'),
        to_team_id=data.get('to_team_id'),
        transfer_type=data.get('transfer_type'),
        amount=data.get('amount')
    )
    
    db.session.add(transfer)
    db.session.commit()
    
    return jsonify({'success': True, 'transfer': transfer.to_dict()})


# ==================== 荣誉 API ====================

@api_bp.route('/awards', methods=['GET'])
def get_awards():
    """获取荣誉榜"""
    coaches = Coach.query.all()
    coaches = sorted(coaches, key=lambda c: c.honor_count, reverse=True)
    
    return jsonify([{
        'id': c.id,
        'game_id': c.game_id,
        'club_name': c.club_name,
        'honor_count': c.honor_count,
        'honors': c.honor_list,
        'rating_display': c.rating_display
    } for c in coaches])


# ==================== 公告 API ====================

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """获取公告"""
    announcements = Announcement.query.order_by(
        Announcement.is_top.desc(),
        Announcement.created_at.desc()
    ).all()
    
    return jsonify([a.to_dict() for a in announcements])


@api_bp.route('/announcements', methods=['POST'])
@login_required
def create_announcement():
    """发布公告"""
    data = request.get_json()
    
    announcement = Announcement(
        title=data.get('title'),
        content=data.get('content'),
        author=data.get('author'),
        is_top=data.get('is_top', False)
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    return jsonify({'success': True, 'announcement': announcement.to_dict()})


# ==================== 统计 API ====================

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    return jsonify({
        'total_teams': Team.query.count(),
        'total_matches': Match.query.count(),
        'total_transfers': Transfer.query.count(),
        'total_coaches': Coach.query.count(),
    })
