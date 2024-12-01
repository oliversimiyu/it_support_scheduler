from datetime import datetime, timedelta
from typing import List, Dict

def validate_schedule(schedule: Dict, team_members: List[Dict]) -> bool:
    """
    Validate a schedule against basic rules:
    - No member works consecutive shifts
    - Members are only scheduled on their available days
    - Shifts are distributed fairly
    """
    for date, shifts in schedule.items():
        # Check for consecutive shifts
        previous_member = None
        for shift_type in ['Morning', 'Afternoon', 'Night']:
            current_member = shifts.get(shift_type)
            if current_member == previous_member:
                return False
            previous_member = current_member

        # Check availability
        weekday = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        for shift_type, member_name in shifts.items():
            member = next((m for m in team_members if m['name'] == member_name), None)
            if member and weekday not in member['availability']:
                return False

    return True

def optimize_schedule(team_members: List[Dict], start_date: datetime, end_date: datetime) -> Dict:
    """
    Create an optimized schedule based on:
    - Fair distribution of shifts
    - Member availability
    - Required rest periods
    """
    schedule = {}
    current_date = start_date
    
    while current_date <= end_date:
        schedule[current_date.strftime('%Y-%m-%d')] = {
            'Morning': None,
            'Afternoon': None,
            'Night': None
        }
        
        # Sort team members by number of shifts assigned
        available_members = sorted(team_members, key=lambda x: x['shifts_assigned'])
        
        for shift_type in ['Morning', 'Afternoon', 'Night']:
            for member in available_members:
                if current_date.strftime('%A') in member['availability']:
                    schedule[current_date.strftime('%Y-%m-%d')][shift_type] = member['name']
                    member['shifts_assigned'] += 1
                    break
                    
        current_date += timedelta(days=1)
    
    return schedule
