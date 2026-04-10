"""
HEIGO 联赛管理系统 - 管理后台路由
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Admin, Team, Match, Transfer, Coach, Announcement

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """管理员登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            flash('登录成功！', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def admin_logout():
    """管理员登出"""
    logout_user()
    return redirect(url_for('main_bp.index'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """管理面板"""
    stats = {
        'teams': Team.query.count(),
        'matches': Match.query.count(),
        'transfers': Transfer.query.count(),
        'coaches': Coach.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/teams')
@login_required
def manage_teams():
    """管理球队"""
    teams = Team.query.all()
    return render_template('admin/teams.html', teams=teams)


@admin_bp.route('/matches')
@login_required
def manage_matches():
    """管理比赛"""
    matches = Match.query.order_by(Match.round).all()
    return render_template('admin/matches.html', matches=matches)


@admin_bp.route('/transfers/<int:transfer_id>/confirm', methods=['POST'])
@login_required
def confirm_transfer(transfer_id):
    """确认交易"""
    transfer = Transfer.query.get_or_404(transfer_id)
    transfer.status = 'confirmed'
    db.session.commit()
    flash('交易已确认', 'success')
    return redirect(url_for('admin.manage_transfers'))


@admin_bp.route('/transfers')
@login_required
def manage_transfers():
    """管理交易"""
    transfers = Transfer.query.order_by(Transfer.created_at.desc()).all()
    return render_template('admin/transfers.html', transfers=transfers)


@admin_bp.route('/announcements')
@login_required
def manage_announcements():
    """管理公告"""
    announcements = Announcement.query.all()
    return render_template('admin/announcements.html', announcements=announcements)
