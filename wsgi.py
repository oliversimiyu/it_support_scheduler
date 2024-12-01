from app import create_app, db
from app.models import User, TeamMember, Shift

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'TeamMember': TeamMember,
        'Shift': Shift
    }

if __name__ == '__main__':
    app.run(debug=True)
