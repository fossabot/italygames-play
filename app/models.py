from flask_login import UserMixin

# Imports application and login manager
from app import db, lm

"""Create helper table for user and game relationship"""
usergames = db.Table('usergames', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('game_isr', db.Integer, db.ForeignKey('games.id')))


class User(UserMixin, db.Model):
    """Defines user table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

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
                            backref='games',
                            lazy='dynamic')

    def __repr__(self):
        return '<Game: {}>'.format(self.name)
