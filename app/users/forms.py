from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    """WTForm for users to edit profile"""
    email = StringField('E-mail', validators=[Email()])
    submit = SubmitField('Save')
