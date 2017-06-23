from flask import url_for, redirect
from flask_login import login_user, current_user
from flask_testing import TestCase

from app import create_app, db
from app.admin.forms import GameForm
from app.models import User, Game


class TestViews(TestCase):
    def create_app(self):
        app = create_app('testing')
        app.app_context().push()

        # Mock method, this assumes OAuth login works, but is needed
        # for testing purposes
        @app.route('/test_login', methods=['GET', 'POST'])
        def test_login():
            user = User.query.first()
            login_user(user)
            return redirect(url_for('games.list'))

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_mock_user(self, admin=False):
        if admin:
            user = User(username='test_user', social_id='123test', is_admin=1)
        else:
            user = User(username='test_user', social_id='123test')
        db.session.add(user)
        db.session.commit()
        return user

    def create_mock_game(self):
        game = Game(name='test_game')
        db.session.add(game)
        db.session.commit()
        return game

    def test_mock_game(self):
        game = self.create_mock_game()
        self.assertEqual(game, Game.query.first())

    def test_mock_user(self):
        user = self.create_mock_user()
        self.assertEqual(user, User.query.first())

    def test_homepage(self):
        res = self.client.get(url_for('home.homepage'))
        self.assert200(res)
        self.assert_template_used('home/index.html')
        self.assertIn('<h1>ItalyGames Play</h1>', res.data)

    def test_login(self):
        with self.client:
            user = self.create_mock_user()
            res = self.client.get(url_for('test_login'), follow_redirects=True)
            self.assert200(res)
            self.assertFalse(current_user.is_anonymous)
            self.assertIn(str(user.username), res.data)

    def test_login_admin(self):
        with self.client:
            user = self.create_mock_user(admin=True)
            res = self.client.get(url_for('test_login'), follow_redirects=True)
            self.assert200(res)
            self.assertTrue(current_user.is_admin)

    def test_login_redirect(self):
        login = url_for('auth.oauth_authorize', provider='reddit')
        res = self.client.get(login)
        self.assertStatus(res, 302)

    def test_login_already_logged_redirect(self):
        self.create_mock_user()
        self.client.get(url_for('test_login'), follow_redirects=True)
        login = url_for('auth.oauth_authorize', provider='reddit')
        res = self.client.get(login)
        self.assertStatus(res, 302)

    def test_logout(self):
        with self.client:
            user = self.create_mock_user()
            res = self.client.get(url_for('test_login'), follow_redirects=True)
            self.assert200(res)
            res = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assert200(res)
            self.assertTrue(current_user.is_anonymous)
            user = db.session.merge(user)
            self.assertNotIn(str(user.username), res.data)

    def test_logout_redirect(self):
        target = url_for('auth.logout')
        redirect = url_for('home.homepage', next=target)
        res = self.client.get(target)
        self.assertStatus(res, 302)
        self.assertRedirects(res, redirect)

    def test_admin_302_when_not_authenticated(self):
        self.assertStatus(
            self.client.get(url_for('admin.list_games')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.add_game')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.edit_game', id=1)), 302)
        self.assertStatus(
            self.client.get(url_for('admin.delete_game', id=1)), 302)

    def test_admin_403_when_not_admin(self):
        with self.client:
            self.create_mock_user()
            res = self.client.get(url_for('test_login'), follow_redirects=True)
            self.assert200(res)
            self.assertFalse(current_user.is_admin)
            self.assertStatus(
                self.client.get(url_for('admin.list_games')), 403)
            self.assertStatus(
                self.client.get(url_for('admin.add_game')), 403)
            self.assertStatus(
                self.client.get(url_for('admin.edit_game', id=1)), 403)
            self.assertStatus(
                self.client.get(url_for('admin.delete_game', id=1)), 403)

    # TODO: create admin tests
    def test_admin_list_games(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user(admin=True)
            self.client.get(url_for('test_login'), follow_redirects=True)
            res = self.client.get(url_for('admin.list_games'))
            self.assert200(res)
            self.assert_template_used('admin/games/games.html')

            game = db.session.merge(game)
            self.assertIn(str(game.name), res.data)

    def test_admin_add_game(self):
        with self.client:
            self.create_mock_user(admin=True)
            game = Game(name='test_game')
            self.client.get(url_for('test_login'), follow_redirects=True)
            form = GameForm(obj=game)
            res = self.client.get(
                url_for('admin.add_game'),
                data=form.data,
                follow_redirects=True)
            self.assert200(res)
            # TODO: find how to test WTForms
            # self.assert_template_used('admin/games/games.html')
            # self.assertTrue(Game.query.count(), 1)

    def test_admin_edit_game(self):
        with self.client:
            self.create_mock_user(admin=True)
            game = self.create_mock_game()
            self.client.get(url_for('test_login'), follow_redirects=True)
            game.name = 'edited'
            form = GameForm(obj=game)
            game = db.session.merge(game)
            res = self.client.get(
                url_for('admin.edit_game', id=game.id),
                data=form.data,
                follow_redirects=True)
            self.assert200(res)
            # TODO: find how to test WTForms
            # self.assertEqual(Game.query.first().name,'edited')

    def test_admin_delete_game(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user(admin=True)
            self.client.get(url_for('test_login'), follow_redirects=True)
            game = db.session.merge(game)
            self.assertTrue(Game.query.count(), 1)
            res = self.client.post(url_for('admin.delete_game', id=game.id),
                                   follow_redirects=True)
            self.assert200(res)
            self.assertEqual(Game.query.count(), 0)

    def test_games_list_not_logged_in(self):
        game = self.create_mock_game()
        res = self.client.get(url_for('games.list'))
        self.assert200(res)
        self.assert_template_used('games/games.html')

        game = db.session.merge(game)
        self.assertIn(str(game.name), res.data)

    def test_games_list_logged_in(self):
        with self.client:
            self.create_mock_game()
            self.create_mock_user()
            res = self.client.get(url_for('test_login'), follow_redirects=True)
            self.assert200(res)
            self.assert_template_used('games/games.html')
            self.assertIn(str(Game.query.first().name), res.data)
            # Check that the additional follow column is rendered
            self.assertIn('/follow/', res.data)

    def test_game_by_id(self):
        game = self.create_mock_game()
        res = self.client.get(url_for('games.get_by_id', id=game.id))
        self.assert200(res)
        self.assert_template_used('games/game.html')
        self.assertIn(str(game.name), res.data)

    def test_game_follow(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user()
            self.client.get(url_for('test_login'), follow_redirects=True)
            game = db.session.merge(game)
            user = db.session.merge(user)
            res = self.client.get(
                url_for('games.follow', game_id=game.id, user_id=user.id),
                follow_redirects=True)
            self.assert200(res)
            self.assert_template_used('games/games.html')
            self.assertIn(Game.query.first(), User.query.first().games)

    def test_game_unfollow(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user()
            self.client.get(url_for('test_login'), follow_redirects=True)

            user = db.session.merge(user)
            game = db.session.merge(game)
            user.add_game(game)
            db.session.commit()
            res = self.client.get(
                url_for('games.unfollow', game_id=game.id, user_id=user.id),
                follow_redirects=True)
            self.assert200(res)
            self.assert_template_used('games/games.html')
            self.assertNotIn(Game.query.first(), User.query.first().games)

    def test_game_filter_by_user(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user()
            user.add_game(game)
            db.session.commit()
            res = self.client.get(
                url_for('games.filter_by_user', username=user.username))
            self.assert200(res)
            self.assert_template_used('games/games.html')
            game = db.session.merge(game)
            self.assertIn(str(game.name), res.data)

    def test_games_search(self):
        # TODO: implement
        pass

    def test_users_list(self):
        user = self.create_mock_user()
        res = self.client.get(url_for('users.list'))
        self.assert200(res)
        self.assert_template_used('users/users.html')
        user = db.session.merge(user)
        self.assertIn(str(user.username), res.data)

    def test_users_get_by_username(self):
        user = self.create_mock_user()
        res = self.client.get(
            url_for('users.get_by_username', username=user.username))
        self.assert200(res)
        self.assert_template_used('users/user.html')
        self.assertIn(str(user.username), res.data)

    def test_users_filter_by_game(self):
        with self.client:
            game = self.create_mock_game()
            user = self.create_mock_user()
            user.add_game(game)
            db.session.commit()
            res = self.client.get(
                url_for('users.filter_by_game', game_id=game.id))
            self.assert200(res)
            self.assert_template_used('users/users.html')
            user = db.session.merge(user)
            self.assertIn(str(user.username), res.data)

    def test_users_search(self):
        # TODO: implement
        pass

    def test_users_edit_profile(self):
        # TODO: implement
        pass
