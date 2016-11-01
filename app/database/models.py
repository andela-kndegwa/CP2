from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    The User Model models the User of this API
    who can be created or allowed to register and
    allowed to log in.

    In Case one tries to access the password attirbute,
    an non-readable attribute error is raised.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class BucketList(db.Model):
    """
    We need a ONE TO ONE relationship
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)



class BucketListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
