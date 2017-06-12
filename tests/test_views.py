from flask import url_for
from flask_login import login_user, logout_user, current_user
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Game


class TestViews(TestCase):
    render_templates = False

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        logout_user()
        db.session.remove()
        db.drop_all()

    @staticmethod
    def create_and_login_mock_user(admin=False):
        if admin:
            user = User(username='test_user', social_id='123test', is_admin=1)
        else:
            user = User(username='test_user', social_id='123test')
        login_user(user)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def create_mock_game():
        game = Game(name='test_game')
        db.session.add(game)
        db.session.commit()
        return game

    def test_homepage(self):
        response = self.client.get(url_for('home.homepage'))
        self.assert200(response)
        self.assert_template_used('home/index.html')
        # self.assertIn('<h1>ItalyGames Play</h1>', response.data)

    def test_login(self):
        self.create_and_login_mock_user()
        self.assertFalse(current_user.is_anonymous)

    def test_login_redirect(self):
        login = url_for('auth.oauth_authorize', provider='reddit')
        response = self.client.get(login)
        self.assertStatus(response, 302)

    def test_login_already_logged_redirect(self):
        self.create_and_login_mock_user()
        login = url_for('auth.oauth_authorize', provider='reddit')
        response = self.client.get(login)
        self.assertStatus(response, 302)

    def test_logout(self):
        self.create_and_login_mock_user()
        self.client.get(url_for('auth.logout'),
                        follow_redirects=True)
        # TODO: Why does this test fail? It logs out in browser
        self.assertFalse(current_user.is_anonymous)

    def test_logout_redirect(self):
        target = url_for('auth.logout')
        redirect = url_for('home.homepage', next=target)
        response = self.client.get(target)
        self.assertStatus(response, 302)
        self.assertRedirects(response, redirect)

    def test_admin_302_when_not_authenticated(self):
        self.assertStatus(
            self.client.get(url_for('admin.list_games')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.add_game')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.edit_game', id=1)), 302)
        self.assertStatus(
            self.client.get(url_for('admin.delete_game', id=1)), 302)

    def test_admin_302_when_not_admin(self):
        self.create_and_login_mock_user()
        self.assertFalse(current_user.is_admin)
        self.assertStatus(
            self.client.get(url_for('admin.list_games')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.add_game')), 302)
        self.assertStatus(
            self.client.get(url_for('admin.edit_game', id=1)), 302)
        self.assertStatus(
            self.client.get(url_for('admin.delete_game', id=1)), 302)

    # TODO: create admin tests
    def test_admin_list_games(self):
        pass

    def test_admin_add_game(self):
        pass

    def test_admin_edit_game(self):
        pass

    def test_admin_delete_game(self):
        pass

    def test_games_list(self):
        response = self.client.get(url_for('games.list'))
        self.assert200(response)
        self.assert_template_used('games/games.html')

    def test_game_by_id(self):
        game = self.create_mock_game()
        response = self.client.get(url_for('games.get_by_id', id=game.id))
        self.assert200(response)
        self.assert_template_used('games/game.html')

    def test_game_follow(self):
        game = self.create_mock_game()
        user = self.create_and_login_mock_user()
        response = self.client.get(
            url_for('games.follow', game_id=game.id, user_id=current_user.id),
            follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('games/games.html')
        # TODO: why does it fail?
        # self.assertIn(current_user.id, User.query.first().games)

    def test_game_unfollow(self):
        game = self.create_mock_game()
        user = self.create_and_login_mock_user()
        user.add_game(game)
        db.session.commit()
        self.assertIn(game, User.query.first().games)
        response = self.client.get(
            url_for('games.unfollow', game_id=game.id, user_id=current_user.id),
            follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('games/games.html')
        self.assertNotIn(game, User.query.first().games)

    def test_game_filter_by_user(self):
        game = self.create_mock_game()
        user = self.create_and_login_mock_user()
        user.add_game(game)
        db.session.commit()
        response = self.client.get(
            url_for('games.filter_by_user', username=current_user.username))
        self.assert200(response)
        self.assert_template_used('games/games.html')

    def test_users_list(self):
        self.create_and_login_mock_user()
        response = self.client.get(url_for('users.list'))
        self.assert200(response)
        self.assert_template_used('users/users.html')

    def test_users_get_by_username(self):
        self.create_and_login_mock_user()
        response = self.client.get(
            url_for('users.get_by_username', username=current_user.username))
        self.assert200(response)
        self.assert_template_used('users/user.html')

    def test_users_filter_by_game(self):
        game = self.create_mock_game()
        user = self.create_and_login_mock_user()
        user.add_game(game)
        db.session.commit()
        response = self.client.get(
            url_for('users.filter_by_game', game_id=game.id))
        self.assert200(response)
        self.assert_template_used('users/users.html')

    def test_users_edit_profile(self):
        # TODO: implement
        pass
