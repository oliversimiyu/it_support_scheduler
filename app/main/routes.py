from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, TeamMember, Shift
from app.main.forms import AssignShiftForm
from app import db
from sqlalchemy import func

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    # Get today's date
    today = datetime.now().date()
    
    # Get current user's team member if they are one
    team_member = None
    if not current_user.is_admin:
        team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    
    # Get today's shifts
    todays_shifts = Shift.query.filter_by(date=today).order_by(Shift.shift_type).all()
    
    # Get upcoming shifts for the next 7 days
    end_date = today + timedelta(days=7)
    upcoming_shifts = Shift.query.filter(
        Shift.date > today,
        Shift.date <= end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    # If user is a team member, get their specific shifts
    my_shifts = []
    if team_member:
        my_shifts = Shift.query.filter(
            Shift.team_member_id == team_member.id,
            Shift.date >= today
        ).order_by(Shift.date, Shift.shift_type).all()
    
    # Get all team members for the admin view
    team_members = TeamMember.query.all() if current_user.is_admin else []
    
    # Calculate some statistics
    total_shifts = len(upcoming_shifts) + len(todays_shifts)
    shifts_per_type = {
        'Morning': sum(1 for s in upcoming_shifts + todays_shifts if s.shift_type == 'Morning'),
        'Afternoon': sum(1 for s in upcoming_shifts + todays_shifts if s.shift_type == 'Afternoon'),
        'Night': sum(1 for s in upcoming_shifts + todays_shifts if s.shift_type == 'Night')
    }
    
    return render_template('dashboard.html',
                         title='Dashboard',
                         todays_shifts=todays_shifts,
                         upcoming_shifts=upcoming_shifts,
                         my_shifts=my_shifts,
                         team_members=team_members,
                         total_shifts=total_shifts,
                         shifts_per_type=shifts_per_type)

@bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = AssignShiftForm()
    
    if form.validate_on_submit():
        shift = Shift(
            date=form.date.data,
            shift_type=form.shift_type.data,
            team_member_id=form.team_member.data
        )
        db.session.add(shift)
        try:
            db.session.commit()
            flash('Shift assigned successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error assigning shift. Please try again.', 'danger')
    
    # Get all shifts ordered by date and type
    shifts = Shift.query.order_by(Shift.date.desc(), Shift.shift_type).all()
    return render_template('schedule.html', title='Schedule', form=form, shifts=shifts)

@bp.route('/my_schedule')
@login_required
def my_schedule():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not team_member:
        flash('You are not assigned as a team member.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Get all shifts for this team member
    shifts = Shift.query.filter_by(team_member_id=team_member.id)\
        .order_by(Shift.date.desc(), Shift.shift_type).all()
    
    return render_template('my_schedule.html', title='My Schedule', 
                         shifts=shifts, team_member=team_member)

@bp.route('/analytics')
@login_required
def analytics():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get shift distribution by type
    shift_distribution = db.session.query(
        Shift.shift_type,
        func.count(Shift.id).label('count')
    ).group_by(Shift.shift_type).all()
    
    shift_types = [s[0] for s in shift_distribution]
    shift_counts = [s[1] for s in shift_distribution]
    
    # Get shifts per team member
    team_member_shifts = db.session.query(
        TeamMember.name,
        func.count(Shift.id).label('count')
    ).join(Shift).group_by(TeamMember.name).all()
    
    member_names = [m[0] for m in team_member_shifts]
    member_shift_counts = [m[1] for m in team_member_shifts]
    
    # Get shifts by day of week
    shifts_by_day = db.session.query(
        func.strftime('%w', Shift.date).label('day'),
        func.count(Shift.id).label('count')
    ).group_by('day').order_by('day').all()
    
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_counts = [0] * 7
    for day, count in shifts_by_day:
        day_counts[int(day)] = count
    
    return render_template('analytics.html',
                         title='Analytics',
                         shift_types=shift_types,
                         shift_counts=shift_counts,
                         member_names=member_names,
                         member_shift_counts=member_shift_counts,
                         days=days,
                         day_counts=day_counts)
