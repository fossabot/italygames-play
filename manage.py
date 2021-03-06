import os
import sys

import coverage
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app, db

COV = coverage.coverage(branch=True, include='app/*')
COV.start()

config_name = os.getenv('FLASK_CONFIG') or 'development'
new_app = create_app(config_name)
manager = Manager(new_app)

# Adds flask-migrate
manager.add_command('db', MigrateCommand)


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', default=8000)
@manager.option('-w', '--workers', dest='workers', type=int, default=3)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return new_app

    # Hacky! Do not pass any cmdline options to gunicorn!
    sys.argv = sys.argv[:2]
    application = FlaskApplication()
    return application.run()


@manager.command
def create_db():
    """Creates db structure"""
    db.create_all()


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    if coverage:
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
    COV.erase()

    # Exit process with error if failed tests
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    manager.run()
