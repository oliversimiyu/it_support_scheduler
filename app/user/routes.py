from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.user import bp
from app.models import User, TeamMember, Shift
from app import db
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not team_member:
        flash('You are not assigned as a team member.', 'warning')
        return redirect(url_for('main.index'))
    
    today = datetime.now().date()
    end_date = today + timedelta(days=30)  # Expand to 30 days for more comprehensive analysis
    
    # Upcoming Shifts
    upcoming_shifts = Shift.query.filter(
        Shift.team_member_id == team_member.id,
        Shift.date >= datetime.now().date()
    ).order_by(Shift.date).all()
    
    # Shift Distribution Analysis
    team_shifts = Shift.query.filter(
        Shift.date >= today,
        Shift.date <= end_date
    ).all()
    
    shift_distribution = {
        'Morning': len([s for s in team_shifts if s.shift_type == 'Morning']),
        'Afternoon': len([s for s in team_shifts if s.shift_type == 'Afternoon']),
        'Night': len([s for s in team_shifts if s.shift_type == 'Night'])
    }
    
    # Personal Workload Analysis
    personal_shifts = Shift.query.filter(
        Shift.team_member_id == team_member.id,
        Shift.date >= today,
        Shift.date <= end_date
    ).all()
    
    personal_shift_distribution = {
        'Morning': len([s for s in personal_shifts if s.shift_type == 'Morning']),
        'Afternoon': len([s for s in personal_shifts if s.shift_type == 'Afternoon']),
        'Night': len([s for s in personal_shifts if s.shift_type == 'Night'])
    }
    
    # Team Workload Analysis
    team_members = TeamMember.query.all()
    workload_data = []
    workload_labels = []
    
    for member in team_members:
        member_shifts = Shift.query.filter(
            Shift.team_member_id == member.id,
            Shift.date >= today,
            Shift.date <= end_date
        ).count()
        
        workload_data.append(member_shifts)
        workload_labels.append(member.name)
    
    return render_template('user/dashboard.html',
                         team_member=team_member,
                         upcoming_shifts=upcoming_shifts,
                         shift_distribution=shift_distribution,
                         personal_shift_distribution=personal_shift_distribution,
                         workload_labels=workload_labels,
                         workload_data=workload_data)

@bp.route('/my_schedule')
@login_required
def my_schedule():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not team_member:
        flash('You are not assigned as a team member.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    today = datetime.now().date()
    # Get all shifts for this team member
    shifts = Shift.query.filter_by(team_member_id=team_member.id)\
        .filter(Shift.date >= today)\
        .order_by(Shift.date).all()
    
    # Group shifts by month for better organization
    shifts_by_month = {}
    for shift in shifts:
        month_key = shift.date.strftime('%B %Y')
        if month_key not in shifts_by_month:
            shifts_by_month[month_key] = []
        shifts_by_month[month_key].append(shift)
    
    return render_template('user/my_schedule.html',
                         shifts=shifts,
                         shifts_by_month=shifts_by_month,
                         team_member=team_member,
                         today=today)

@bp.route('/team_schedule')
@login_required
def team_schedule():
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    
    # Get all shifts for the team in the next 7 days
    team_shifts = Shift.query.filter(
        Shift.date >= today,
        Shift.date <= end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    # Organize shifts by date and shift type
    team_schedule = {}
    for shift in team_shifts:
        if shift.date not in team_schedule:
            team_schedule[shift.date] = {
                'Morning': None,
                'Afternoon': None,
                'Night': None
            }
        team_schedule[shift.date][shift.shift_type] = shift
    
    # Get upcoming shifts
    upcoming_shifts = team_shifts
    
    # Get user's personal shifts
    my_shifts = Shift.query.join(TeamMember).filter(
        TeamMember.user_id == current_user.id,
        Shift.date >= today,
        Shift.date <= end_date
    ).order_by(Shift.date, Shift.shift_type).all()
    
    # Shift Distribution Analysis
    shift_distribution = {
        'Morning': len([s for s in team_shifts if s.shift_type == 'Morning']),
        'Afternoon': len([s for s in team_shifts if s.shift_type == 'Afternoon']),
        'Night': len([s for s in team_shifts if s.shift_type == 'Night'])
    }
    
    # Team Member Workload Analysis
    team_members = TeamMember.query.all()
    workload_data = []
    workload_labels = []
    
    for member in team_members:
        member_shifts = Shift.query.filter(
            Shift.team_member_id == member.id,
            Shift.date >= today,
            Shift.date <= end_date
        ).count()
        
        workload_data.append(member_shifts)
        workload_labels.append(member.name)
    
    return render_template('user/team_schedule.html',
                         team_schedule=team_schedule,
                         upcoming_shifts=upcoming_shifts,
                         my_shifts=my_shifts,
                         shift_distribution=shift_distribution,
                         workload_labels=workload_labels,
                         workload_data=workload_data)

@bp.route('/profile')
@login_required
def profile():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    return render_template('user/profile.html', team_member=team_member)

@bp.route('/update_availability', methods=['POST'])
@login_required
def update_availability():
    team_member = TeamMember.query.filter_by(user_id=current_user.id).first()
    if not team_member:
        flash('You are not assigned as a team member.', 'warning')
        return redirect(url_for('user.profile'))
    
    availability = request.form.getlist('availability[]')
    team_member.availability = ','.join(availability)
    db.session.commit()
    
    flash('Your availability has been updated.', 'success')
    return redirect(url_for('user.profile'))
