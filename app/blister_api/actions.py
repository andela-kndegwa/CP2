from flask import g, jsonify
from app import db
from flask_restful import abort
from models import BucketListItem, User, BucketList


def save(record):
    db.session.add(record)
    db.session.commit()


def delete(record):
    db.session.delete(record)
    db.session.commit()


def update():
    db.session.commit()


def create_bucketlist(data):
    """
    Attributes:
    Title: Title of the bucket list
    Description : Description of the bucket list.

    """
    if not data:
        abort(400, 'Please add information for your bucketlist.')
    if not data.get('title'):
        abort(400, 'Please provide a title for your bucketlist')

    title = data.get('title')
    description = data.get('description')
    user_id = g.user.id

    bucket_list_title_exists = BucketList.query.filter_by(title=title).first()
    current_user = BucketList.query.filter_by(user_id=user_id).first()
    if bucket_list_title_exists and current_user:
        abort(400, message='Two bucket lists cannot have the same title.')
    bucketlist = BucketList(title=title,
                            description=description,
                            user_id=user_id)
    save(bucketlist)
    return {'bucketlist': bucketlist}


def update_bucketlist(data, bucketlist_id):
    # import pdb;pdb.set_trace()
    if not data:
        abort(400, 'Please add information for your bucketlist.')
    bucketlist = BucketList.query.filter_by(id=bucketlist_id,
                                            user_id=g.user.id).first_or_404()
    if not bucketlist:
        abort(404, 'Bucket list not found.')
    title = data.get('title', bucketlist.title)
    description = data.get('description', bucketlist.description)
    bucketlist.title = title
    bucketlist.description = description
    update()
    return {'bucketlist': bucketlist}


def delete_bucket_list(bucketlist_id):
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first_or_404()
    delete(bucketlist)


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
        abort(401, message=user)
    else:
        return user


def retrieve_particular_bucketlist(bucketlist_id):
    bucketlist = BucketList.query.filter(BucketList.id == bucketlist_id)
    return bucketlist


def retrieve_all_bucketlists():
    """
    This accesses the global variable to be able to access the
    user object that contains user details and information.
    """
    bucketlists = BucketList.query.filter(
        BucketList.user_id == g.user.id).all()
    return bucketlists
