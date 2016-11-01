import os
import random
import string
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''
    This is the main configuration class that allows
    the production, development and testing databases to
    be created and configured from scratch with appropriate settings.
    '''
    SECRET_KEY = ''.join(random.choice(
        string.ascii_uppercase + string.digits)for x in xrange(32))
    # The above generates a random and hard to guess string
    # and stores it in the SECRET_KEY variable.
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    DEBUG = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blister-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blister-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blister.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# The above allows us to import all the above configuration in one
# dictionary.
