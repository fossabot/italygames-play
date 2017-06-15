from flask import abort, render_template, redirect, url_for, request

from . import games
from .. import db
from ..models import Game, User

PER_PAGE = 10


@games.route('/games', defaults={'page': 1})
@games.route('/games/page/<int:page>')
def list(page):
    """Gets list of games ordered by followers and paginates"""
    games = Game.query \
        .order_by(Game.num_of_users.desc()) \
        .paginate(page, PER_PAGE, error_out=False)

    return render_template('games/games.html',
                           games=games,
                           title='Games')


@games.route('/game/<int:id>')
def get_by_id(id):
    """Returns a single game by ID"""
    game = Game.query.get_or_404(id)

    return render_template('games/game.html',
                           game=game,
                           title=game.name)


@games.route('/game/<int:game_id>/follow/<int:user_id>',
             methods=['GET', 'POST'])
def follow(game_id, user_id):
    """Follows games based on user and game ids. See implementation
    details on models.py"""
    game = Game.query.get_or_404(game_id)
    user = User.query.get_or_404(user_id)
    user.add_game(game)
    db.session.commit()

    return redirect(url_for('games.list'))


@games.route('/game/<int:game_id>/unfollow/<int:user_id>',
             methods=['GET', 'POST'])
def unfollow(game_id, user_id):
    """Unfollows games based on user and game ids. See implementation
    details on models.py"""
    game = Game.query.get_or_404(game_id)
    user = User.query.get_or_404(user_id)
    user.remove_game(game)
    db.session.commit()

    return redirect(url_for('games.list'))


@games.route('/user/<string:username>/games', defaults={'page': 1})
@games.route('/user/<string:username>/games/page/<int:page>')
def filter_by_user(username, page):
    """Returns all of a single user"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    games = Game.query \
        .filter(Game.users.contains(user)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('games/games.html',
                           games=games,
                           title='Games of ' + username)


@games.route('/games/search', methods=['POST'])
def search():
    name = request.form.get('query')
    if name is None:
        abort(404)
    return redirect(url_for('games.search_results', name=name, page=1))


@games.route('/games/search/<string:name>', defaults={'page': 1})
@games.route('/games/search/<string:name>/page/<int:page>')
def search_results(name, page):
    games = Game.query \
        .filter(Game.name.contains(name)) \
        .paginate(page, PER_PAGE, error_out=None)

    return render_template('games/games.html',
                           games=games,
                           title='Search')
