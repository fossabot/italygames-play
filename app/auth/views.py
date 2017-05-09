from flask import flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .. import db
from ..models import User
from oauth import OAuthSignIn


# TODO: comments
@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.dashboard'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('home.dashboard'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username = oauth.callback()

    if social_id is None:
        flash('Authentication failed')
        return redirect(url_for('home'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    return redirect(url_for('home.dashboard'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
