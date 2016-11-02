from datetime import datetime
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.blister import app
from sqlalchemy.orm import relationship


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
    bucket_list = relationship("BucketList", uselist=False,
                               back_populates="user")

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

    def generate_authentication_token(self, expiration=1200):
        """
        Token Based authentication begins here.


        Arguments:
        expiration = 1200 seconds i.e 20 Minutes
        """
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        This verifies the authentication token within the session.
        A static method is used as a user will only
        be known after the token is decoded.
        """
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            """Valid but expired token. """
            return None
        except BadSignature:
            """Invalid token """
            return None
        user_id = data['id']
        return user_id

    def __repr__(self):
        return "<User: %r>" % self.username


class BucketList(db.Model):
    """
    The Bucket List Model establishes
    a Bucket List model where items can
    be added to.
    """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates='bucket_list')

    def __repr__(self):
        return "<Bucketlist: %r>" % self.title


class BucketListItem(db.Model):
    """
    This represents the individual bucket list items.
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

    def __repr__(self):
        return "<Bucketlist item: %r>" % self.title
