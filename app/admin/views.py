from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import GameForm
from .. import db
from ..models import Game


def check_admin():
    """Prevents non-admins from accessing the page"""
    if not current_user.is_admin:
        abort(403)


@admin.route('/games', methods=['GET', 'POST'])
@login_required
def list_games():
    """List all games"""
    check_admin()
    games = Game.query.all()

    return render_template('admin/games/games.html',
                           games=games,
                           title='Games')


@admin.route('/games/add', methods=['GET', 'POST'])
@login_required
def add_game():
    """Adds game to database"""
    check_admin()
    add_game = True
    form = GameForm()

    if form.validate_on_submit():
        game = Game(name=form.name.data)

        try:
            db.session.add(game)
            db.session.commit()
            flash('Game successfully added')
        except:
            flash('Error: game name already exists')

        return redirect(url_for('admin.list_games'))

    return render_template('admin/games/game.html',
                           action='Add',
                           add_game=add_game,
                           form=form,
                           title='Add Game')


@admin.route('/games/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_game(id):
    """Edit extisting game"""
    check_admin()
    add_game = False
    game = Game.query.get_or_404(id)
    form = GameForm(obj=game)

    if form.validate_on_submit():
        game.name = form.name.data
        db.session.commit()
        flash('Game successfully edited')

        return redirect(url_for('admin.list_games'))

    form.name.data = game.name

    return render_template('admin/games/game.html',
                           action='Edit',
                           add_game=add_game,
                           form=form,
                           game=game,
                           title='Edit Game')


@admin.route('/games/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_game(id):
    """Delete existing game"""
    check_admin()
    game = Game.query.get_or_404(id)

    db.session.delete(game)
    db.session.commit()
    flash('Game successfully deleted')

    return redirect(url_for('admin.list_games'))
    return render_template(title='Delete Game')
