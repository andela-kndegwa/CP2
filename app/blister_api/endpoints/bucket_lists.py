from flask import request, jsonify
from flask_restplus import abort, Resource
from app import api
from app.blister_api.serializer import bucket_list_item, bucket_list
from app.blister_api.models import BucketList
from app.blister_api.actions import create_bucket_list


ns = api.namespace(
    'bucketlists',
    description="Operations related to individual bucket lists.")


@ns.route('/')
@api.response(200, 'Success')
class BucketListCollection(Resource):
    """
    This method retrieves all the bucket lists associcated
    with a particular user.
    """
    @api.marshal_with(bucket_list)
    def get(self):
        '''
        This shows a list of all the bucket lists.
        '''
        bucket_lists = BucketList.query.all()
        if not bucket_lists:
            message = 'There are no bucket lists as of now'
            return jsonify(message)
        else:
            return jsonify(bucket_lists), 200

    @api.marshal_with(bucket_list)
    def post(self):
        pass

    @api.expect(bucket_list)
    def put(self):
        pass

    def delete(self):
        pass
