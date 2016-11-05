from flask import g
from models import User
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


@auth.verify_password
def authenticate_token(token, password):
    """Autheticate User with the provided token."""
    user = User.verify_auth_token(token)
    if user:
        g.user = user
        return True
    return False
