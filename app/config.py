import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''
    This is the main configuration class that allows
    the production, development and testing databases to
    be created and configured from scratch with appropriate settings.
    '''
    SECRET_KEY = 'LERHEX8EKDZIPR8O3ZF26Z4IDA9AWPFS'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    DEBUG = True
    ERROR_404_HELP = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'blister-dev.sqlite')


class TestingConfig(Config):
    db_name = 'blister-test.sqlite'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, db_name)


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'blister.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# The above allows us to import all the above configuration in one
# dictionary.
