from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from app.models import TeamMember

class AssignShiftForm(FlaskForm):
    team_member = SelectField('Team Member', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    shift_type = SelectField('Shift Type', 
                           choices=[('Morning', 'Morning'), 
                                  ('Afternoon', 'Afternoon'), 
                                  ('Night', 'Night')],
                           validators=[DataRequired()])
    submit = SubmitField('Assign Shift')

    def __init__(self, *args, **kwargs):
        super(AssignShiftForm, self).__init__(*args, **kwargs)
        self.team_member.choices = [(m.id, f"{m.name} ({m.role})") 
                                  for m in TeamMember.query.all()]
