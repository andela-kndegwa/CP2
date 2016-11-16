from flask_restful import Resource, reqparse, fields, marshal_with
from app.blister_api.actions import login_user


class LoginUser(Resource):
    def __init__(self):
        self.login_user_parser = reqparse.RequestParser()
        self.login_user_parser.add_argument('username',
                                            type=str, required=True,
                                            location='json')
        self.login_user_parser.add_argument('password',
                                            type=str, required=True,
                                            location='json')
        super(LoginUser, self).__init__()

    @marshal_with({'token': fields.String})
    def post(self):
        data = self.login_user_parser.parse_args()
        user = login_user(data)
        token = user.generate_authentication_token()
        return {'token': token.decode('utf-8')}, 201
