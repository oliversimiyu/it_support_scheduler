import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from colorama import init, Fore, Style
from models.database import init_db, TeamMember, Shift

# Initialize colorama for colored console output
init()

class ITSupportScheduler:
    def __init__(self):
        self.team_members = []
        self.schedules = {}
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.ensure_data_directory()
        self.db_session = init_db()

    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def add_team_member(self, name, role, availability=None):
        """Add a new team member"""
        member = {
            'name': name,
            'role': role,
            'availability': availability or ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'shifts_assigned': 0
        }
        self.team_members.append(member)
        
        # Add to database
        db_member = TeamMember(
            name=name,
            role=role,
            availability=','.join(member['availability'])
        )
        self.db_session.add(db_member)
        self.db_session.commit()
        
        print(f"{Fore.GREEN}Added team member: {name} ({role}){Style.RESET_ALL}")

    def create_schedule(self, start_date, end_date):
        """Create a new schedule for the specified date range"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        dates = pd.date_range(start=start_date, end=end_date)
        schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon', 'Night'])
        schedule.fillna('Unassigned', inplace=True)
        self.schedules[start_date] = schedule
        
        # Load existing assignments from database
        existing_shifts = self.db_session.query(Shift).filter(
            Shift.date >= start_date,
            Shift.date <= end_date
        ).all()
        
        for shift in existing_shifts:
            schedule.at[shift.date, shift.shift_type] = shift.team_member.name
            
        return schedule

    def assign_shift(self, date, shift, member_name):
        """Assign a shift to a team member"""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
            
        success = False
        for schedule_date, schedule in self.schedules.items():
            if date in schedule.index:
                # Check if the member is already assigned to another shift on this date
                member_shifts = schedule.loc[date]
                if member_name in member_shifts.values:
                    print(f"{Fore.RED}Error: {member_name} is already assigned to a shift on {date}{Style.RESET_ALL}")
                    return False
                
                schedule.at[date, shift] = member_name
                success = True
                
                # Add to database
                db_shift = Shift(
                    date=date,
                    shift_type=shift,
                    team_member_id=self.db_session.query(TeamMember).filter_by(name=member_name).first().id
                )
                self.db_session.add(db_shift)
                self.db_session.commit()
                
                for member in self.team_members:
                    if member['name'] == member_name:
                        member['shifts_assigned'] += 1
                print(f"{Fore.BLUE}Assigned {member_name} to {shift} shift on {date}{Style.RESET_ALL}")
                break
                
        if not success:
            print(f"{Fore.RED}No schedule found for date: {date}{Style.RESET_ALL}")
            return False
            
        return True

    def display_schedule(self, start_date):
        """Display the schedule for a specific period"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
        if start_date in self.schedules:
            print(f"\n{Fore.YELLOW}Schedule from {start_date}:{Style.RESET_ALL}")
            print(self.schedules[start_date].to_string())
        else:
            print(f"{Fore.RED}No schedule found for the specified date.{Style.RESET_ALL}")

    def display_team_stats(self):
        """Display statistics for team members"""
        print(f"\n{Fore.CYAN}Team Statistics:{Style.RESET_ALL}")
        for member in self.team_members:
            print(f"{member['name']} ({member['role']}): {member['shifts_assigned']} shifts")

def main():
    scheduler = ITSupportScheduler()
    
    # Demo data
    scheduler.add_team_member("John Doe", "Senior Support Engineer")
    scheduler.add_team_member("Jane Smith", "Support Engineer")
    scheduler.add_team_member("Mike Johnson", "Support Engineer")
    
    # Create a schedule for the next week
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    schedule = scheduler.create_schedule(today, next_week)
    
    # Convert today to datetime for pandas index compatibility
    today_dt = pd.Timestamp(today)
    
    # Assign some shifts
    scheduler.assign_shift(today_dt, 'Morning', 'John Doe')
    scheduler.assign_shift(today_dt, 'Afternoon', 'Jane Smith')
    scheduler.assign_shift(today_dt, 'Night', 'Mike Johnson')
    
    # Display the schedule
    scheduler.display_schedule(today)
    scheduler.display_team_stats()

if __name__ == "__main__":
    main()
