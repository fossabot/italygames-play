from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    """WTForm for admins to add or edit game"""
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
