from flask_testing import TestCase

from app import create_app, db
from app.models import User, Game


class TestModels(TestCase):
    def create_app(self):
        app = create_app('testing')
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_create(self):
        user = User(username='test_user', social_id='123test')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_user_delete(self):
        user = User(username='test_user', social_id='123test')
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 0)

    def test_user_edit(self):
        user = User(username='test_user', social_id='123test')
        db.session.add(user)
        db.session.commit()
        user.username = 'edited'
        db.session.commit()
        self.assertEqual(User.query.first(), user)

    def test_user_addgame(self):
        user = User(username='test_user', social_id='123test')
        game = Game(name='test_game')
        db.session.add(user)
        db.session.add(game)
        user.add_game(game)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 1)
        self.assertIn(Game.query.first(), User.query.first().games)

    def test_user_addgame_two_games(self):
        user = User(username='test_user', social_id='123test')
        game1 = Game(name='test_game1')
        game2 = Game(name='test_game2')
        db.session.add(user)
        db.session.add(game1)
        db.session.add(game2)
        user.add_game(game1)
        user.add_game(game2)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 2)
        self.assertIn(game1, User.query.first().games)
        self.assertIn(game2, User.query.first().games)

    def test_user_addgame_twice(self):
        user = User(username='test_user', social_id='123test')
        game = Game(name='test_game')
        db.session.add(user)
        db.session.add(game)
        user.add_game(game)
        user.add_game(game)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 1)
        self.assertIn(Game.query.first(), User.query.first().games)

    def test_user_removegame(self):
        user = User(username='test_user', social_id='123test')
        game = Game(name='test_game')
        db.session.add(user)
        db.session.add(game)
        user.add_game(game)
        db.session.commit()
        user.remove_game(game)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 0)
        self.assertNotIn(Game.query.first(), User.query.first().games)

    def test_user_removegame_not_related(self):
        user = User(username='test_user', social_id='123test')
        game1 = Game(name='test_game1')
        game2 = Game(name='test_game2')
        db.session.add(user)
        db.session.add(game1)
        user.add_game(game1)
        db.session.commit()
        user.remove_game(game2)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 1)
        self.assertIn(Game.query.first(), User.query.first().games)

    def test_user_removegame_twice(self):
        user = User(username='test_user', social_id='123test')
        game = Game(name='test_game')
        db.session.add(user)
        db.session.add(game)
        user.add_game(game)
        db.session.commit()
        user.remove_game(game)
        user.remove_game(game)
        db.session.commit()
        self.assertEqual(User.query.first().games.count(), 0)
        self.assertNotIn(Game.query.first(), User.query.first().games)

    def test_game_create(self):
        game = Game(name='test_game')
        db.session.add(game)
        db.session.commit()
        self.assertEqual(Game.query.count(), 1)

    def test_game_delete(self):
        game = Game(name='test_game')
        db.session.add(game)
        db.session.commit()
        db.session.delete(game)
        db.session.commit()
        self.assertEqual(Game.query.count(), 0)

    def test_game_edit(self):
        game = Game(name='test_game')
        db.session.add(game)
        db.session.commit()
        game.name = 'edited'
        db.session.commit()
        self.assertEqual(Game.query.first(), game)
