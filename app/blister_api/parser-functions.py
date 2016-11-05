from flask_restplus import reqparse

# This validates user credentials on create user
user_credentials = reqparse.RequestParser()
user_credentials.add_argument(
    'username', type=str, required=True, location='json')
user_credentials.add_argument(
    'password', type=str, required=True, location='json')
