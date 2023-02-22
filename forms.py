from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[
                            DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("Submit")

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=4, max=255)])
    description = StringField ('Description')
    completed = BooleanField('Completed')
    team_assigned = SelectField(u'Team Assigned')
    submit = SubmitField("Submit")

    def update_teams(self, teams):
        self.team_assigned.choices = [ (team.id, team.name) for team in teams ]