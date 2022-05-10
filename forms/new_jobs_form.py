from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class NewJobForm(FlaskForm):
    jobs = TextAreaField('Job title')
    lead = IntegerField('Team leader id', validators=[DataRequired()])
    size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = TextAreaField('Collaborators')
    finish = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
