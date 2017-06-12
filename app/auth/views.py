"""
Routes for auth module
"""

from flask import flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .. import db
from ..models import User
from oauth import OAuthSignIn


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    """
    Handles auth call to OAuth provider

    Obtains the specified provider authorize method and calls it.

    Parameters
    ----------
    provider : str
        Provider name corresponding to the OAuthSignIn.provider_name
    """
    if not current_user.is_anonymous:
        return redirect(url_for('games.list'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    """
    Handles redirect back from OAuth provider

    Obtains the specified provider callback method and calls it for
    authentication. If successful checks the db and register new user when
    necessary. Then logins via flask-login and redirects to the dashboard.

    Parameters
    ----------
    provider : str
        Provider name corresponding to the OAuthSignIn.provider_name
    """
    if not current_user.is_anonymous:
        return redirect(url_for('games.list'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username = oauth.callback()

    if social_id is None:
        flash('Authentication failed')
        return redirect(url_for('home.homepage'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user)

    return redirect(url_for('games.list'))


@auth.route('/logout')
@login_required
def logout():
    """Log user out of the session via flask-login"""
    logout_user()
    return redirect(url_for('home.homepage'))
