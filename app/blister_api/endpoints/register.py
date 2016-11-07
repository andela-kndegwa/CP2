from flask_restful import Resource, reqparse, fields, marshal_with
from app.blister_api.actions import register_user


class RegisterUser(Resource):
    def __init__(self):
        self.register_user_parser = reqparse.RequestParser()
        self.register_user_parser.add_argument('username',
                                               type=str, required=True,
                                               location='json')
        self.register_user_parser.add_argument('email',
                                               type=str, required=True,
                                               location='json')
        self.register_user_parser.add_argument('password',
                                               type=str, required=True,
                                               location='json')
        super(RegisterUser, self).__init__()

    def post(self):
        data = self.register_user_parser.parse_args()
        register_user(data)
        return {'Message': 'Sign Up successful. Please log in to use the service.'}, 201
