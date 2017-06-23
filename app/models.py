from string import lower

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import select, func, event
from sqlalchemy.ext.hybrid import hybrid_property

from app import db, lm

"""Create helper table for user and game relationship"""
usergames = db.Table('usergames', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('game_id', db.Integer, db.ForeignKey('games.id')))


class User(UserMixin, db.Model):
    """Defines user table"""
    __tablename__ = 'users'

    id        = db.Column(db.Integer, primary_key=True)
    bio       = db.Column(db.Text, nullable=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username  = db.Column(db.String(64), nullable=False, unique=True)
    email     = db.Column(db.String(64), nullable=True, unique=True)
    is_admin  = db.Column(db.Boolean, default=False)
    socials   = db.relationship('UserSocialID',
                              backref=db.backref('user'),
                              lazy='dynamic')

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

    def add_social_id(self, user_social_id):
        """Given a UserSocialID upserts it"""
        self.remove_social_id(user_social_id)
        self.socials.append(user_social_id)
        return self

    def remove_social_id(self, user_social_id):
        """Remove UserSocialID"""
        if self.has_social_id(user_social_id):
            self.socials.remove(user_social_id)
        return self

    def has_social_id(self, user_social_id):
        """Check that user had a given UserSocialID"""
        return self.socials \
                   .filter_by(social_id=user_social_id.social_id) \
                   .count() > 0

    def get_socials_dict(self):
        """Returns existing social usernames in a dict object"""
        socials_dict = {}
        for social_id in self.socials.all():
            socials_dict[social_id.social.name] = social_id.user_social_id
        return socials_dict

    def set_socials_by_form(self, social_form):
        """Expects SocialForm() in input, then upserts all social usernames"""

        # Get social platform name and social username set by user and iterate
        for social_name, user_social_id in social_form.data.iteritems():
            # Check that social platforms exists
            social = Social.query \
                .filter(func.lower(Social.name) == social_name) \
                .first()
            if social is not None:
                # Check that user had already a username set for that platform
                social_id = UserSocialID.query.get((self.id, social.id))
                if social_id is None:
                    # If not create new UserSocialID
                    social_id = UserSocialID(user_id=self.id,
                                             social_id=social.id,
                                             user_social_id=user_social_id)
                else:
                    # Else update existing
                    social_id.user_social_id = user_social_id
                # Upsert new/updated social username
                self.add_social_id(social_id)

        return self

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Game(db.Model):
    """Defines game table"""
    __tablename__ = 'games'

    id   = db.Column(db.Integer, primary_key=True)
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


class Social(db.Model):
    """Defines social table"""

    __tablename__ = 'socials'

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(64), nullable=False)
    url   = db.Column(db.String(256), nullable=True)
    users = db.relationship('UserSocialID',
                            backref=db.backref('social'),
                            lazy='dynamic')


class UserSocialID(db.Model):
    """Many to many association table for user -> social"""
    __tablename__ = 'usersocialids'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    social_id = db.Column(db.Integer,
                          db.ForeignKey('socials.id'),
                          primary_key=True)
    user_social_id = db.Column(db.String(64), nullable=False)


# Populate Social table with default data
@event.listens_for(Social.__table__, 'after_create')
def populate(*args, **kwargs):
    socials = ['Reddit', 'Telegram', 'Discord', 'Steam', 'Origin', 'Blizzard']
    for social_name in socials:
        db.session.add(Social(name=social_name))
    db.session.commit()
