import os

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app, db

config_name = os.getenv('FLASK_CONFIG')
manager = Manager(create_app(config_name))

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


if __name__ == '__main__':
    manager.run()