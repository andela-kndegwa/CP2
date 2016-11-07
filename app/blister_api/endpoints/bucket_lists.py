from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with


from app.blister_api.authentication import multi_auth
from app.blister_api.serializer import bucketlist_serializer, bucketlist_collection_serializer
from app.blister_api.actions import create_bucketlist, retrieve_all_bucketlists


from app.blister_api.models import BucketList


class BucketListCollection(Resource):
    """
    This class retrieves all the bucket lists associcated
    with a particular user.

    Its initialised using the reqparse module from which
    we get the RequestParser class and proceed to create
    an instance of it which is used to validate arguments
    parsed to the BucketList Resource.
    """
    decorators = [multi_auth.login_required]

    def __init__(self):
        self.bucket_list_parser = reqparse.RequestParser()
        self.bucket_list_parser.add_argument('title', type=str,
                                             required=True,
                                             help='Please provide a title for your bucketlist.',
                                             location='json')
        self.bucket_list_parser.add_argument(
            'description', type=str, location='json')
        self.bucket_list_parser.add_argument(
            'Authorization', location='headers')
        super(BucketListCollection, self).__init__()

    @marshal_with(bucketlist_serializer)
    def post(self):
        data = self.bucket_list_parser.parse_args()
        create_bucketlist(data)

    @marshal_with(bucketlist_collection_serializer)
    def get(self):
        bucketlists = retrieve_all_bucketlists()
        return bucketlists
