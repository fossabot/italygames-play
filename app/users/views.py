from flask import abort, render_template
from flask_login import login_required

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


@users.route('/user/<string:username>/edit')
@login_required
def edit_profile(username):
    pass
