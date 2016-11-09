from flask import request, jsonify
from flask_restful import Resource, reqparse, marshal_with
from app import api
# from app.blister_api.serializer import bucket_list_item
from app.blister_api.models import BucketListItem
from app.blister_api.authentication import multi_auth


from app.blister_api.serializer import bucketlist_serializer
from app.blister_api.serializer import bucketlistitem_serializer
from app.blister_api.actions import retrieve_particular_bucketlist_item, retrieve_all_bucketlists_items
from app.blister_api.actions import create_bucket_list_item
from app.blister_api.actions import update_bucket_list_item


# ns = api.namespace(
#     'bucketlists/items/',
#     description="Operations related to bucket lists items.")


class BucketListItemCollection(Resource):
    """
    This method retrieves all the bucket lists associcated
    with a particular user.
    """
    decorators = [multi_auth.login_required]

    def __init__(self):
        self.item_parser = reqparse.RequestParser()
        self.item_parser.add_argument('title', type=str,
                                      required=True,
                                      help='Please provide a title for your bucketlist item.',
                                      location='json')
        self.item_parser.add_argument(
            'description', type=str, location='json')
        self.item_parser.add_argument(
            'bucketlist_id', type=int, location='json')
        self.item_parser.add_argument(
            'done', type=int, location='json')
        super(BucketListItemCollection, self).__init__()

    @marshal_with(bucketlist_serializer)
    def get(self, bucketlist_id=None, item_id=None):
        if bucketlist_id:
            items = retrieve_particular_bucketlist_item(bucketlist_id)
            return {'items': items}, 200
        items = retrieve_all_bucketlists_items()
        return {'items': items}, 200

    @marshal_with(bucketlistitem_serializer)
    def post(self, bucketlist_id=None, item_id=None):
        data = self.item_parser.parse_args()
        item = create_bucket_list_item(data)
        return {'item': item}, 201

    @marshal_with(bucketlist_serializer)
    def put(self, bucketlist_id=None, item_id=None):
        data = self.item_parser.parse_args()
        item = update_bucket_list_item(data, item_id)
        return {'item': item}
