import logging
from logging import StreamHandler

# Third-party imports
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import app_config

db = SQLAlchemy()
lm = LoginManager()


def create_app(config_name):
    """Initiates all the dependencies and returns app instance"""
    app = Flask(__name__, instance_relative_config=True)

    # Loads config.py
    app.config.from_object(app_config[config_name])

    # Bootstrap setup
    Bootstrap(app)

    # db setup
    db.init_app(app)

    # Login manager setup
    lm.init_app(app)
    lm.login_message = "You must be logged in to access this page"
    lm.login_view = "home.homepage"

    # Migrate setup
    migrate = Migrate(app, db)

    # Logging setup
    handler = StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # Imports all the blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .games import games as games_blueprint
    app.register_blueprint(games_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # Error handling
    # Redirects to HTTP error pages
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    # Route necessary for letsencrypt certbot
    @app.route('/.well-known/acme-challenge/<token_value>')
    def letsencrypt(token_value):
        with open('.well-known/acme-challenge/{}'.format(token_value)) as f:
            answer = f.readline().strip()
        return answer

    # Session handling
    # Necessary to refresh sessions and reflect data changes
    @app.before_request
    def startup_session():
        db.session = db.create_scoped_session()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.close()

    return app
