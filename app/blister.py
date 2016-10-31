from app import create_app, api
from flask_restplus import Resource

# from app import create_app
app = create_app('development')


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """
                this is a very interesting ui
        """
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run()
