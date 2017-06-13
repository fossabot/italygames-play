from flask import abort
from flask_testing import TestCase

from app import create_app, db


class TestViews(TestCase):
    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_403_forbidden(self):
        # Create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        res = self.client.get('/403')
        self.assertStatus(res, 403)
        self.assert_template_used('errors/403.html')

    def test_404_not_found(self):
        res = self.client.get('/nothinghere')
        self.assertStatus(res, 404)
        self.assert_template_used('errors/404.html')

    def test_500_internal_server_error(self):
        # Create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        res = self.client.get('/500')
        self.assertStatus(res, 500)
        self.assert_template_used('errors/500.html')
