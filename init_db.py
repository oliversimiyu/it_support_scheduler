from app import create_app, db
from app.models import User, TeamMember, Shift
from datetime import datetime, timedelta

def init_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create regular user
        user = User(
            username='user',
            email='user@example.com',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
        
        db.session.commit()
            
        # Add team members
        team_members = [
            TeamMember(
                name='John Smith',
                role='Senior Support Engineer',
                availability='Monday,Tuesday,Wednesday,Thursday,Friday'
            ),
            TeamMember(
                name='Sarah Johnson',
                role='Support Engineer',
                availability='Monday,Tuesday,Wednesday,Thursday,Friday'
            ),
            TeamMember(
                name='Mike Wilson',
                role='Support Engineer',
                availability='Monday,Tuesday,Wednesday,Thursday,Friday'
            ),
            TeamMember(
                name='Emily Brown',
                role='Junior Support Engineer',
                availability='Monday,Tuesday,Wednesday,Thursday,Friday'
            ),
            TeamMember(
                name='David Lee',
                role='Support Engineer',
                availability='Monday,Tuesday,Wednesday,Thursday,Friday'
            )
        ]
        
        for member in team_members:
            db.session.add(member)
        
        db.session.commit()
        
        # Add sample shifts for the next 7 days
        today = datetime.now().date()
        shift_types = ['Morning', 'Afternoon', 'Night']
        
        # Create a rotating schedule for the team members
        for i in range(7):  # Next 7 days
            current_date = today + timedelta(days=i)
            for j, shift_type in enumerate(shift_types):
                # Rotate team members through shifts
                member_index = (i + j) % len(team_members)
                shift = Shift(
                    date=current_date,
                    shift_type=shift_type,
                    team_member_id=team_members[member_index].id
                )
                db.session.add(shift)
        
        db.session.commit()
        print("Database initialized with admin user, team members, and sample shifts.")

if __name__ == '__main__':
    init_database()
