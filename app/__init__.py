from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
api_blueprint = Blueprint("api", __name__, url_prefix='/v1')
api = Api(api_blueprint,version='1.0', title='BucketlisTER',
          description='The BucketlisTER is a bucketlist application API built with Flask.')

def create_app(config_name):
	"""
	The create_app function here is our app factory
	that creates out application and passes only the 
	required configuration


	Argument Parameters : 
	Within our config.py file.
	This is where the configurations are made .i.e
	config_name

	Return value:
	Eventually it returns our app which is fully configured.


	"""
	app = Flask(__name__)
	app.config.from_object(config[config_name]) # dictionary with all the right configurations made
	config[config_name].init_app(app)
	db.init_app(app)
	return app