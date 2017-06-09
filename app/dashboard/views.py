from flask import render_template, redirect, url_for
from flask_login import login_required

from . import dashboard
from .. import db
from ..models import Game, User, usergames


PER_PAGE = 15


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
    return render_template(title='Follow Game')


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
    return render_template(title='Unfollow Game')
