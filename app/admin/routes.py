from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, TeamMember, Shift
from app.admin.forms import CreateAdminForm
from app import db
from app.decorators import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.count()
    total_team_members = TeamMember.query.count()
    total_shifts = Shift.query.count()
    
    # Get recent shifts
    recent_shifts = Shift.query.order_by(Shift.date.desc()).limit(5).all()
    
    # Get shift distribution
    shift_distribution = db.session.query(
        Shift.shift_type,
        func.count(Shift.id).label('count')
    ).group_by(Shift.shift_type).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_team_members=total_team_members,
                         total_shifts=total_shifts,
                         recent_shifts=recent_shifts,
                         shift_distribution=shift_distribution)

@bp.route('/manage-admins', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_admins():
    form = CreateAdminForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('New admin user created successfully!', 'success')
            return redirect(url_for('admin.manage_admins'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating admin user. Please try again.', 'danger')
    
    # Get list of all admin users
    admin_users = User.query.filter_by(is_admin=True).all()
    return render_template('admin/manage_admins.html', 
                         title='Manage Admins',
                         form=form,
                         admin_users=admin_users)

@bp.route('/remove-admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def remove_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot remove yourself as an admin.', 'danger')
        return redirect(url_for('admin.manage_admins'))
    
    user.is_admin = False
    try:
        db.session.commit()
        flash(f'Removed admin privileges from {user.username}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error removing admin privileges. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_admins'))

@bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/manage_users.html',
                         title='Manage Users',
                         users=users)

@bp.route('/manage-team')
@login_required
@admin_required
def manage_team():
    team_members = TeamMember.query.all()
    return render_template('admin/manage_team.html',
                         title='Manage Team',
                         team_members=team_members)

@bp.route('/schedule-management')
@login_required
@admin_required
def schedule_management():
    shifts = Shift.query.order_by(Shift.date.desc()).all()
    team_members = TeamMember.query.all()
    return render_template('admin/schedule_management.html',
                         title='Schedule Management',
                         shifts=shifts,
                         team_members=team_members)

@bp.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('admin/reports.html',
                         title='Reports')
