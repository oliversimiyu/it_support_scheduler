from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, TeamMember

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.admin_login'))
        if not user.is_admin:
            flash('Access denied. This login is for administrators only.', 'danger')
            return redirect(url_for('auth.user_login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.dashboard'))
    return render_template('auth/admin_login.html', title='Admin Login', form=form)

@bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.user_login'))
        if user.is_admin:
            flash('Please use the admin login page.', 'warning')
            return redirect(url_for('auth.admin_login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user.dashboard'))
    return render_template('auth/user_login.html', title='User Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        
        # Link team member if selected
        if form.team_member.data != 0:
            team_member = TeamMember.query.get(form.team_member.data)
            if team_member:
                team_member.user_id = user.id
        
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template('auth/register.html', title='Register', form=form)
