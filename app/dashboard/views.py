from flask import render_template
from flask_login import login_required
from sqlalchemy.sql import func, desc

from . import dashboard
from .. import db
from ..models import Game, usergames


PER_PAGE = 15


@dashboard.route('/')
@login_required
def homepage():
    """Renders dashboard template if logged in"""
    return render_template('dashboard/index.html', title='Dashboard')


@dashboard.route('/games', defaults={'page': 1})
@dashboard.route('/games/page/<int:page>')
@login_required
def games_list(page):
    games = db.session.query(Game.id, Game.name, Game.num_of_users) \
        .order_by(Game.num_of_users.desc()) \
        .paginate(page, PER_PAGE, error_out=False)

    return render_template('dashboard/games/games.html',
                           games=games,
                           title='Games')


@dashboard.route('/game/<int:id>')
@login_required
def view_game(id):
    pass
