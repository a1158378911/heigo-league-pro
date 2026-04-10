"""
HEIGO 足球经理联赛管理系统 - 数据模型
支持：积分榜、比赛、赛程、交易、荣誉
"""
from datetime import datetime
from app import db


class Team(db.Model):
    """球队模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='球队名称')
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), comment='教练 ID')
    league_level = db.Column(db.String(20), nullable=False, default='甲级', comment='联赛级别')
    
    # 统计数据
    played = db.Column(db.Integer, default=0, comment='场次')
    won = db.Column(db.Integer, default=0, comment='胜')
    drawn = db.Column(db.Integer, default=0, comment='平')
    lost = db.Column(db.Integer, default=0, comment='负')
    goals_for = db.Column(db.Integer, default=0, comment='进球')
    goals_against = db.Column(db.Integer, default=0, comment='失球')
    points = db.Column(db.Integer, default=0, comment='积分')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    coach = db.relationship('Coach', backref='teams')
    matches_home = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team')
    matches_away = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team')
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'coach_name': self.coach.game_id if self.coach else '未知',
            'league_level': self.league_level,
            'played': self.played,
            'won': self.won,
            'drawn': self.drawn,
            'lost': self.lost,
            'goals_for': self.goals_for,
            'goals_against': self.goals_against,
            'goal_difference': self.goal_difference,
            'points': self.points,
        }


class Match(db.Model):
    """比赛模型"""
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False, comment='轮次')
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_score = db.Column(db.Integer, default=0, comment='主队比分')
    away_score = db.Column(db.Integer, default=0, comment='客队比分')
    match_date = db.Column(db.Date, comment='比赛日期')
    status = db.Column(db.String(20), default='pending', comment='状态：pending/finished')
    match_type = db.Column(db.String(20), default='league', comment='类型：league/cup')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'round': self.round,
            'home_team': self.home_team.name if self.home_team else '未知',
            'away_team': self.away_team.name if self.away_team else '未知',
            'home_score': self.home_score,
            'away_score': self.away_score,
            'match_date': self.match_date.strftime('%Y-%m-%d') if self.match_date else '',
            'status': self.status,
            'match_type': self.match_type,
        }


class Transfer(db.Model):
    """交易模型"""
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False, comment='球员姓名')
    position = db.Column(db.String(20), comment='位置')
    from_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), comment='转出球队')
    to_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), comment='转入球队')
    transfer_type = db.Column(db.String(20), nullable=False, comment='类型：买卖/交换/自由签约')
    amount = db.Column(db.Integer, comment='交易金额')
    status = db.Column(db.String(20), default='pending', comment='状态：pending/confirmed')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    from_team = db.relationship('Team', foreign_keys=[from_team_id], backref='transfers_from')
    to_team = db.relationship('Team', foreign_keys=[to_team_id], backref='transfers_to')
    
    def to_dict(self):
        return {
            'id': self.id,
            'player_name': self.player_name,
            'position': self.position,
            'from_team': self.from_team.name if self.from_team else '未知',
            'to_team': self.to_team.name if self.to_team else '未知',
            'transfer_type': self.transfer_type,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else '',
        }


class Coach(db.Model):
    """教练模型（保留原有结构）"""
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(100), nullable=False, comment='游戏 ID')
    club_name = db.Column(db.String(200), nullable=False, comment='执教俱乐部')
    league_level = db.Column(db.String(20), nullable=False, default='甲级', comment='联赛级别')
    join_date = db.Column(db.String(50), comment='加入联赛时间')
    forum_id = db.Column(db.String(100), comment='论坛 ID')
    career = db.Column(db.Text, comment='职业生涯')
    rating = db.Column(db.String(1), nullable=False, default='C', comment='评级 S/A/B/C')
    stars = db.Column(db.Integer, nullable=False, default=1, comment='星级 1-5')
    honors = db.Column(db.Text, default='', comment='冠军荣誉')
    avatar = db.Column(db.String(500), default='', comment='头像 URL')
    motto = db.Column(db.String(500), default='', comment='座右铭')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def honor_list(self):
        if not self.honors:
            return []
        return [h.strip() for h in self.honors.split(',') if h.strip()]
    
    @property
    def honor_count(self):
        return len(self.honor_list)
    
    @property
    def rating_display(self):
        return f"{self.rating or 'C'}{self.stars or 1}"


class Announcement(db.Model):
    """公告模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='标题')
    content = db.Column(db.Text, nullable=False, comment='内容')
    author = db.Column(db.String(100), comment='发布者')
    is_top = db.Column(db.Boolean, default=False, comment='是否置顶')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'is_top': self.is_top,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }


class Admin(db.Model):
    """管理员模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }
