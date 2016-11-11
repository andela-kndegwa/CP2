from flask_restful import Resource, reqparse
from app.blister_api.actions import register_user


class Home(Resource):
    def get(self):
        return 'Welcome to blister!'


class RegisterUser(Resource):
    def __init__(self):
        self.register_user_parser = reqparse.RequestParser()
        self.register_user_parser.add_argument('username',
                                               type=str, required=True,
                                               location='json')
        self.register_user_parser.add_argument('password',
                                               type=str, required=True,
                                               location='json')
        super(RegisterUser, self).__init__()

    def post(self):
        data = self.register_user_parser.parse_args()
        register_user(data)
        return 'Sign Up successful. Please log in.', 201
