from datetime import datetime

from flask import current_app
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)
from sqlalchemy.orm import relationship
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
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    bucket_list = relationship("BucketList")

    @property
    def password(self):
        """
        This renders the password attribute inaccessible.
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        This static method passes the above password
        property and generates a password hash.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        The verify password is key in establishing
        that the password hash is indeed passed.

        Arguments:
        password. Takes the password property and verifies
        its existence.
        """
        return check_password_hash(self.password_hash, password)

    def generate_authentication_token(self, expires_in=30):
        """
        Token Based authentication begins here.


        Arguments:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """
        This verifies the authentication token within the session.
        A static method is used as a user will only
        be known after the token is decoded.

        Raise the more specific ERROR for the None
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            import pdb
            pdb.set_trace()
            data = s.loads(token)
        except SignatureExpired:
            """Valid but expired token. """
            return None
        except BadSignature:
            """Invalid token """
            return None
        user_id = data['id']
        return user_id

    @staticmethod
    def query_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user is None:
            # User does not exist
            return 'Authentication failed.'
        if not user.verify_password(password):
            # Password verification failed
            return 'Authentication failed.'
        return user

    def __repr__(self):
        return "<User: %r>" % self.username


class BucketList(db.Model):
    """
    The Bucket List Model establishes
    a Bucket List model where items can
    be added to.

    Relationship:
    The Bucket List has a one to many relationship
    with the User.
    """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    completed = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="bucket_list")

    @staticmethod
    def query_bucket_list(bucket_list_title):
        bucket_list = BucketList.query.filter_by(
            title=bucket_list_title).first()
        if bucket_list is None:
            return 'Bucket list does not exist'
        return bucket_list

    def __repr__(self):
        return "<Bucketlist: %r>" % self.title


class BucketListItem(db.Model):
    """
    This represents the individual bucket list items.

    Relationship:
    The Bucket List Item has a one to many relationship
    with the Buckect List.
    """
    __tablename__ = 'bucketlist_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlists.id"))
    bucketlist = db.relationship('BucketList', backref=db.backref(
        'bucketlist_items', lazy='dynamic'))

    @staticmethod
    def query_item(title):
        item = BucketListItem.query.filter_by(
            title=title).first()
        if item is None:
            return 'Bucket list item does not exist'
        return item

    def __repr__(self):
        return "<Bucketlist item: %r>" % self.title
