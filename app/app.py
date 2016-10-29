from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app, version='1.0', title='BucketlisTER',
          description='The BucketlisTER is a bucketlist application API built with Flask.')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blister.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
    	"""
		this is a very interesting ui
    	"""
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)