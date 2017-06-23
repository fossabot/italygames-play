from string import lower

from flask import abort, render_template, url_for, redirect, request
from flask_login import login_required, current_user

from app import db
from app.users.forms import UserForm, SocialForm
from . import users
from ..models import Game, User

PER_PAGE = 10


@users.route('/users', defaults={'page': 1})
@users.route('/users/page/<int:page>')
def list(page):
    """Render list of users and paginates"""
    users = User.query.paginate(page, PER_PAGE, error_out=False)

    return render_template('users/users.html',
                           users=users,
                           title='Users')


@users.route('/user/<string:username>')
def get_by_username(username):
    """Render user profile based on username"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    return render_template('users/user.html',
                           user=user,
                           title=username)


@users.route('/game/<int:game_id>/users', defaults={'page': 1})
@users.route('/game/<int:game_id>/users/page/<int:page>')
def filter_by_game(game_id, page):
    """Returns list of users filtered by followed game"""
    game = Game.query.get_or_404(game_id)
    users = User.query \
        .filter(User.games.contains(game)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('users/users.html',
                           users=users,
                           title='Users following ' + game.name)


@users.route('/user/<string:username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    """Edit profile"""
    if current_user.username != username:
        abort(403)
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    user_form = UserForm(obj=user)
    # Create SocialForm based on existing user social ids
    social_form = SocialForm(obj=user.get_socials_dict())

    # Check that UserForm is submitted
    if user_form.submit_user.data and user_form.validate_on_submit():
        user.email = user_form.email.data
        user.bio = user_form.bio.data
        db.session.commit()
        return redirect(
            url_for('users.get_by_username', username=user.username))

    # Check that SocialForm is submitted
    if social_form.submit_social.data and social_form.validate_on_submit():
        user.set_socials_by_form(social_form)
        db.session.commit()
        return redirect(
            url_for('users.get_by_username', username=user.username))

    # Renders existing data on forms
    user_form.email.data = user.email
    user_form.bio.data = user.bio
    for social_name, social_id in user.get_socials_dict().iteritems():
        social_form[lower(social_name)].data = social_id

    return render_template('users/edit_profile.html',
                           user_form=user_form,
                           social_form=social_form,
                           user=user,
                           title='Edit Profile')


@users.route('/users/search', methods=['POST'])
def search():
    username = request.form.get('query')
    if username is None:
        abort(404)
    return redirect(url_for('users.search_results', username=username, page=1))


@users.route('/users/search/<string:username>', defaults={'page': 1})
@users.route('/users/search/<string:username>/page/<int:page>')
def search_results(username, page):
    users = User.query \
        .filter(User.username.contains(username)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('users/users.html',
                           users=users,
                           title='Search')
