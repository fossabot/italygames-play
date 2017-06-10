from flask_login import UserMixin
from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property

from app import db, lm

"""Create helper table for user and game relationship"""
usergames = db.Table('usergames', db.Model.metadata,
                     db.Column('user_id', db.Integer,db.ForeignKey('users.id')),
                     db.Column('game_id', db.Integer,db.ForeignKey('games.id')))


class User(UserMixin, db.Model):
    """Defines user table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def add_game(self, game):
        if not self.has_game(game):
            self.games.append(game)
            return self

    def remove_game(self, game):
        if self.has_game(game):
            self.games.remove(game)
            return self

    def has_game(self, game):
        return self.games.filter(usergames.c.game_id == game.id).count() > 0

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Game(db.Model):
    """Defines game table"""

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    # So that we can use game.users and user.games to get list of
    # matching items
    users = db.relationship('User',
                            secondary=usergames,
                            backref=db.backref('games', lazy='dynamic'),
                            lazy='dynamic')

    @hybrid_property
    def num_of_users(self):
        if self.users:
            return self.users.count()
        return 0

    @num_of_users.expression
    def num_of_users(cls):
        return (select([func.count(usergames.c.user_id)])
                .where(cls.id == usergames.c.game_id)
                .label('users_count'))

    def __repr__(self):
        return '<Game: {}>'.format(self.name)
