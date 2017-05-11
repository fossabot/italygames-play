from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    """Form for admin to add or edit game"""
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
