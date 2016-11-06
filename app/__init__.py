from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()  # Initialise the db
api_bp = Blueprint('api', __name__, url_prefix='/api/v1.0')

# Initialise the Api class
api = Api(api_bp)


def create_app(config_name):
    '''
    The creat_app function functions as the application
    factory. This means all the initialization is effected
    here.

    Arguments :
    It takes the config dictionary from the config.py
    and accesses the required class and its properties as
    requried.

    Return value:
    It finally returns the app fully created

    '''
    app_main = Flask(__name__)
    app_main.config.from_object(config[config_name])
    db.init_app(app_main)
    app_main.register_blueprint(api_bp)
    return app_main
