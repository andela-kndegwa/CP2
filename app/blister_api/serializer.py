from flask_restplus import fields
from app import api

bucket_list_item = api.model('Bucket list item', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a bucket list item'),
    'title': fields.String(required=True,
                           description='Bucket list item title'),
    'description': fields.String(description='Bucket list item body or description'),
    'done': fields.Boolean(default=False),
    'date_added': fields.DateTime,
    'date_modified': fields.DateTime,
    'bucketlist_id': fields.Integer(attribute='bucketlists.id'),
    'bucketlist': fields.String(attribute='bucketlists.id')
})

bucket_list = api.model('Bucket list', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a bucket list'),
    'title': fields.String(required=True,
                           description='Bucket list title'),
    'description': fields.String(description='Bucket list body or description'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'user_id': fields.Integer(attribute='users.id'),
    'user': fields.String(attribute='users.id')

})
