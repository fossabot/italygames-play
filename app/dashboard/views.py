from flask import abort, render_template, redirect, url_for
from flask_login import login_required

from . import dashboard
from .. import db
from ..models import Game, User

PER_PAGE = 10


@dashboard.route('/')
@login_required
def homepage():
    """Renders dashboard template if logged in"""
    return render_template('dashboard/index.html', title='Dashboard')


@dashboard.route('/games', defaults={'page': 1})
@dashboard.route('/games/page/<int:page>')
@login_required
def list_games(page):
    """Gets list of games ordered by followers and paginates"""
    games = Game.query \
        .order_by(Game.num_of_users.desc()) \
        .paginate(page, PER_PAGE, error_out=False)

    return render_template('dashboard/games/games.html',
                           games=games,
                           title='Games')


@dashboard.route('/game/<int:id>')
@login_required
def view_game(id):
    """Returns a single game by ID"""
    game = Game.query.get_or_404(id)

    return render_template('dashboard/games/game.html',
                           game=game,
                           title=game.name)


@dashboard.route('/game/<int:game_id>/follow/<int:user_id>',
                 methods=['GET', 'POST'])
@login_required
def follow_game(game_id, user_id):
    """Follows games based on user and game ids. See implementation
    details on models.py"""
    game = Game.query.get_or_404(game_id)
    user = User.query.get_or_404(user_id)
    user.add_game(game)
    db.session.commit()

    return redirect(url_for('dashboard.list_games'))
    # return render_template(title='Follow Game')


@dashboard.route('/game/<int:game_id>/unfollow/<int:user_id>',
                 methods=['GET', 'POST'])
@login_required
def unfollow_game(game_id, user_id):
    """Unfollows games based on user and game ids. See implementation
    details on models.py"""
    game = Game.query.get_or_404(game_id)
    user = User.query.get_or_404(user_id)
    user.remove_game(game)
    db.session.commit()

    return redirect(url_for('dashboard.list_games'))
    # return render_template(title='Unfollow Game')


@dashboard.route('/users', defaults={'page': 1})
@dashboard.route('/users/page/<int:page>')
def list_users(page):
    users = User.query.paginate(page, PER_PAGE, error_out=False)

    return render_template('dashboard/users/users.html',
                           users=users,
                           title='Users')


@dashboard.route('/user/<string:username>')
def view_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    return render_template('dashboard/users/user.html',
                           user=user,
                           title=username)


@dashboard.route('/game/<int:game_id>/users', defaults={'page': 1})
@dashboard.route('/game/<int:game_id>/users/page/<int:page>')
def view_users_per_game(game_id, page):
    game = Game.query.get_or_404(game_id)
    users = User.query \
        .filter(User.games.contains(game)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('dashboard/users/users.html',
                           users=users,
                           title='Users following ' + game.name)


@dashboard.route('/user/<string:username>/games', defaults={'page': 1})
@dashboard.route('/user/<string:username>/games/page/<int:page>')
def view_games_per_user(username, page):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    games = Game.query \
        .filter(Game.users.contains(user)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('dashboard/games/games.html',
                           games=games,
                           title='Games of ' + username)
