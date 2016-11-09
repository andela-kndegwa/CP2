from flask import g
from flask_restful import abort

from app import db
from models import BucketListItem, User, BucketList

# Database save, delete and update functionality.


def save(record):
    db.session.add(record)
    db.session.commit()


def delete(record):
    db.session.delete(record)
    db.session.commit()


def update():
    db.session.commit()

# Ends here.
# -------------------------------------------------
# Actions pertaining to users


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
        abort(400, message='Username or email address added already exist.')
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

# Ends here.
# -------------------------------------------------
# C.R.U.D Operations for the API Begin here
# =================================================
# CREATE bucket list and bucket list items


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
    g.user.bucketlists.append(bucketlist)
    save(bucketlist)
    return {'bucketlist': bucketlist}


def create_bucket_list_item(data):
    '''
    data here is the JSON Object representing
    the request sent with the URI

    Attributes:
    'title' : Title of the blister item
    'description': Extra description for the item
    'bucket': 'String' value highlighting the particular bucket list
    '''
    if not data:
        abort(400, 'Please add information for your bucketlist.')
    if not data.get('title'):
        abort(400, 'Please provide a title for your bucketlist')
    title = data.get('title')
    description = data.get('description')
    bucketlist_id = data.get('bucketlist_id')
    if not bucketlist_id:
        return {'Message': 'Please enter bucketlist_id'}, 400
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
    item = BucketListItem(title=title,
                          description=description,
                          bucketlist_id=bucketlist_id)
    save(item)
    bucketlist.items.append(item)
    return item

# =================================================
# READ bucket list and bucket list items


def retrieve_all_bucketlists():
    """
    This accesses the global variable to be able to access the
    user object that contains user details and information.

    """
    bucketlists = BucketList.query.filter(
        BucketList.user_id == g.user.id).all()
    return bucketlists


def retrieve_particular_bucketlist(bucketlist_id):
    bucketlist = BucketList.query.filter(
        BucketList.id == bucketlist_id).first()
    return bucketlist


def retrieve_particular_bucketlist_item(item_id):
    item = BucketListItem.query.filter(BucketListItem.id == item_id).first()
    return item


def retrieve_all_bucketlists_items():
    """
    This accesses the global variable to be able to access the
    user object that contains user details and information.

    """
    items = BucketListItem.query.filter(
        BucketListItem.bucketlist_id == g.user.bucket_list.id).all()
    return items
# =================================================
# UPDATE  bucket list and bucket list items


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


def update_bucket_list_item(data, item_id):
    if not data:
        abort(400, 'Please add information for your bucketlist item.')
    item = BucketListItem.query.filter_by(id=item_id).first_or_404()
    if not item:
        abort(404, 'Bucket list item not found.')
    title = data.get('title', item.title)
    description = data.get('description', item.description)
    item.title = title
    item.description = description
    update()
    return {'item': item}

# =================================================
# DELETE  bucket list and bucket list items


def delete_bucket_list(bucketlist_id):
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first_or_404()
    delete(bucketlist)


def delete_bucket_list_item(bucketlist_id=None, item_id=None):
    item = BucketListItem.query.filter_by(id=item_id,
                                          bucketlist_id=bucketlist_id).first_or_404()
    delete(item)
    return ''
