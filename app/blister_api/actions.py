from app import db
from models import BucketListItem


def create_bucket_list(data):
    """
    Attributes:
    Title: Title of the bucket list
    Description :

    """
    pass


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
    db.session.add(item)
    db.session.commit()


def update_bucket_list_item():
    pass


def delete_bucket_list_item():
    pass


def register_user():
    pass


def login_user():
    pass


def logout_user():
    pass


def update_user():
    pass


def delete_user():
    pass
