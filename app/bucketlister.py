from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from app import create_app

app = create_app()
api = Api(app, version='1.0', title='BucketlisTER',
          description='The BucketlisTER is a bucketlist application API built with Flask.')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
    	"""
		this is a very interesting ui
    	"""
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)