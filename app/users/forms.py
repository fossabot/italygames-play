from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Email

from ..models import Social

# TODO: add max length validator to fields
class UserForm(FlaskForm):
    """WTForm for users to edit profile"""
    email = StringField('E-mail', validators=[Email()])
    bio = TextAreaField('Bio', render_kw={'rows': 5})
    submit = SubmitField('Save')

class SocialForm(FlaskForm):
    """WTForm for user social profiles"""
    reddit = StringField('Reddit')
    telegram = StringField('Telegram')
    discord = StringField('Discord')
    steam = StringField('Steam')
    origin = StringField('Origin')
    blizzard = StringField('Blizzard')
    submit = SubmitField('Save')
