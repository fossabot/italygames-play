import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Common configurations"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'antani'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {
        'reddit': {
            'id': os.getenv('OAUTH_REDDIT_ID'),
            'secret': os.getenv('OAUTH_REDDIT_SECRET')
        }
    }


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev_db.sqlite')


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    # workaround for Flask-Testing bug
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URI') or \
        'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')


class ProductionConfig(Config):
    """Production configurations"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
