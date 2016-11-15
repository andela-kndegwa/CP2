from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort


from app.blister_api.authentication import multi_auth
from app.blister_api.serializer import (bucketlist_serializer,
                                        bucketlist_collection_serializer)
from app.blister_api.actions import (search_bucket_list,
                                     update_bucketlist,
                                     delete_bucket_list,
                                     create_bucketlist,
                                     retrieve_all_bucketlists,
                                     retrieve_particular_bucketlist)
from app.blister_api.utils import paginate


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
                                             help='Please provide a title for your bucketlist.',
                                             location='json')
        self.bucket_list_parser.add_argument(
            'description', type=str, location='json')
        self.bucket_list_parser.add_argument(
            'Authorization', location='headers')
        super(BucketListCollection, self).__init__()

    @marshal_with(bucketlist_serializer)
    def post(self, id=None):
        if id:
            return {'Message': "Bad Request"}, 400
        data = self.bucket_list_parser.parse_args()
        response = create_bucketlist(data)
        return response, 201

    @marshal_with(bucketlist_collection_serializer)
    @paginate
    def get(self):
        bucketlists = retrieve_all_bucketlists()
        q = request.args.get('q')
        if q:
            bucketlists = search_bucket_list(q)
            if not bucketlists:
                abort(404, message='That bucketlist does not exist.')
            else:
                return bucketlists, 200
        return bucketlists, 200


class SingleBucketList(Resource):
    def __init__(self):
        self.bucket_list_parser = reqparse.RequestParser()
        self.bucket_list_parser.add_argument('title', type=str,
                                             location='json')
        self.bucket_list_parser.add_argument(
            'description', type=str, location='json')
        self.bucket_list_parser.add_argument(
            'Authorization', location='headers')
        super(SingleBucketList, self).__init__()
    decorators = [multi_auth.login_required]

    @marshal_with(bucketlist_serializer)
    def get(self, id=None):
        if id:
            bucketlist = retrieve_particular_bucketlist(id)
            if not bucketlist:
                abort(404, message='That bucketlist does not exist.')
            return bucketlist, 200

    @marshal_with(bucketlist_serializer)
    def put(self, id):
        data = self.bucket_list_parser.parse_args()
        bucketlist = update_bucketlist(data, id)
        return bucketlist, 200

    def delete(self, id=None):
        if id:
            delete_bucket_list(id)
            return {'Message': "Bucket list successfully deleted."}, 204
        else:
            return {'Message': "Bad Request"}, 400
