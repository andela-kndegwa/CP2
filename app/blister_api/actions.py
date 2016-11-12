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
    Parameters:
    Data here is the JSON Object representing
    the request sent with the URI.

    Requires:
    username and password to perform user registeration.

    Returns:
    The actual user with a 201 Success response for
    the POST.
    '''
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        abort(400, message='Please enter a username and password to register.')
    username_exists = User.query.filter_by(username=username).first()
    if username_exists:
        abort(400, message='Username added already exist.')
    user = User(username=username, password=password)
    save(user)
    return user


def login_user(data):
    """
    Parameters:
    Data here is the JSON Object representing
    the request sent with the URI with actual credentials
    in the database.

    Requires:
    username and password to perform login.

    Returns:
    The user.
    If the return is a message, it returns the error message.

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
        abort(400, message='Please add information for your bucketlist.')
    if not data.get('title'):
        abort(400, message='Please provide a title for your bucketlist')

    title = data.get('title')
    description = data.get('description')
    user_id = g.user.id

    bucket_list_title_exists = BucketList.query.filter_by(title=title).first()
    current_user = User.query.filter_by(id=user_id).first()
    if bucket_list_title_exists and current_user:
        abort(400, message='Two bucket lists cannot have the same title.')
    bucketlist = BucketList(title=title,
                            description=description,
                            user_id=user_id)
    g.user.bucketlists.append(bucketlist)
    save(bucketlist)
    return bucketlist


def create_bucket_list_item(data, bucketlist_id):
    '''
    data here is the JSON Object representing
    the request sent with the URI

    Attributes:
    'title' : Title of the blister item
    'description': Extra description for the item
    'bucket': 'String' value highlighting the particular bucket list

    In case the bucket list does not belong to a user,
    an error message is returned.
    '''
    if not data:
        abort(400, message='Please add information for your bucketlist item.')
    if not data.get('title'):
        abort(400, message='Please provide a title for your bucketlist item')
    title = data.get('title')
    description = data.get('description')
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
    item_title_exists = BucketListItem.query.filter_by(title=title).first()
    if item_title_exists:
        abort(400, message='Two bucket lists cannot have the same title.')
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
    bucketlist = BucketList.query.filter_by(
        id=bucketlist_id).first()
    if not bucketlist:
        abort(404, message='Bucket list not found.')
    if bucketlist.user_id != g.user.id:
        return abort(401,
                     message="Unauthorized access." +
                     "You do not own that bucket list.")
    return bucketlist


def search_bucket_list(query):
    bucketlists = g.user.bucketlists\
        .filter(BucketList.title.contains(query)).all()
    return bucketlists


def retrieve_particular_bucketlist_item(bucketlist_id, item_id):
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
    if bucketlist.user_id != g.user.id:
        return abort(401,
                     message="Unauthorized access." +
                     "You do not own that bucket list.")
    item = BucketListItem.query.filter_by(
        id=item_id, bucketlist_id=bucketlist_id).first()
    return item


def retrieve_all_bucketlists_items(bucketlist_id):
    """
    This accesses the global variable to be able to access the
    user object that contains user details and information.

    """
    bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
    if bucketlist.user_id != g.user.id:
        return abort(401,
                     message="Unauthorized access." +
                     "You do not own that bucket list.")
    items = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
    return items
# =================================================
# UPDATE  bucket list and bucket list items


def update_bucketlist(data, bucketlist_id):
    if not data:
        abort(400, 'Please add information for your bucketlist.')
    bucketlist = BucketList.query.filter_by(id=bucketlist_id,
                                            user_id=g.user.id).first()
    if not bucketlist:
        abort(404, 'Bucket list not found.')
    title = data.get('title', bucketlist.title)
    description = data.get('description', bucketlist.description)
    bucketlist.title = title
    bucketlist.description = description
    update()
    return bucketlist


def update_bucket_list_item(data, item_id):
    if not data:
        abort(400, 'Please add information for your bucketlist item.')
    item = BucketListItem.query.filter_by(id=item_id).first_or_404()
    if not item:
        abort(404, 'Bucket list item not found.')
    title = data.get('title', item.title)
    description = data.get('description', item.description)
    done = data.get('done', False)
    item.title = title
    item.description = description
    item.done = done
    update()
    return item

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

# =================================================
# SEARCH bucket list and bucket list items
