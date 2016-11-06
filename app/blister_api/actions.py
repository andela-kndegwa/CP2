from flask import g
from app import db
from flask_restful import abort
from models import BucketListItem, User, BucketList


def save(record):
    db.session.add(record)
    db.session.commit()


def validate_data_is_sent(data):
    if not data:
        abort(400, 'No data sent. Please add the required information')
    return data


def create_bucketlist(data):
    """
    Attributes:
    Title: Title of the bucket list
    Description :

    """
    data = validate_data_is_sent(data)
    if not data.get('title'):
        abort(400, 'Please provide a title for your bucketlist')
    title = data.get('title')
    description = data.get('description')
    user_id = data.get('user_id')
    user = User.query.filter(User.id == user_id).one()
    bucketlist = BucketList(title=title, description=description,
                            user_id=user_id, user=user)
    g.user.bucket_list.append(bucketlist)
    save(bucketlist)
    return {'Bucket list': '%s added successfully'} % title, 201


def update_bucket_list():
    pass


def delete_bucket_list():
    pass


def create_bucket_list_item(data):
    '''
    data here is the JSON Object representing
    the request sent with the URI

    Attributes:
    'title' : Title of the blister item
    'description': Extra description for the item
    'bucket': 'String' value highlighting the particular bucket list
    '''
    title = data.get('title')
    description = data.get('description', '')
    # bucketlist = data.get('bucketlist')
    item = BucketListItem(title=title,
                          description=description)
    save(item)


def update_bucket_list_item():
    pass


def delete_bucket_list_item():
    pass


def register_user(data):
    '''
    data here is the JSON Object representing
    the request sent with the URI
    '''
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        abort(400, message='Please enter a username, email and password to register.')
    username_exists = User.query.filter_by(username=username).first()
    email_exists = User.query.filter_by(email=email).first()
    if email_exists or username_exists:
        abort(400, message='Either the username or email address added already exist.')
    user = User(username=username, password=password, email=email)
    save(user)
    return user


def login_user(data):
    """

    """
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        abort(400, message='Please enter a username and password to log in.')
    user = User.query_user(username, password)
    if type(user) == str:
        abort(400, message=user)
    else:
        return user


def logout_user():
    pass


def update_user():
    pass


def delete_user():
    pass
