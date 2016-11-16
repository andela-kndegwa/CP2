from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from app.blister_api.models import User


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if User.verify_password(password):
            g.user = username
            return True
        return False


@token_auth.verify_token
def verify_token(token):
    user_id = User.verify_auth_token(token)
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
        return True
    return False
