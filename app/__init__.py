import logging
from logging import StreamHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import app_config

db = SQLAlchemy()
lm = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)

    # login manager setup
    lm.init_app(app)
    lm.login_message = "You must be logged in to access this page"
    lm.login_view = "home.homepage"

    # migrate setup
    migrate = Migrate(app, db)

    # logging setup
    handler = StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
