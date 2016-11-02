from flask import request, jsonify
from flask_restplus import Resource
from app import api
from app.blister_api.serializer import bucket_list_item, bucket_list
from app.blister_api.actions import create_bucket_list
from app.database import models


ns = api.namespace(
    'blister/bucket_lists',
    description="Options related to individual bucket lists.")


@ns.route('/')
class BucketListCollection(Resource):
    """
    This method retrieves all the bucket lists associcated
    with a particular user.
    """
    @api.marshal_list_with(bucket_list)
    def get(self):
        '''
        This shows a list of all the bucket lists.
        '''
        bucket_lists = models.BucketList.query.all()
        if bucket_lists is None:
            return {'Message': 'There are no bucket lists as of now'}
        return bucket_lists

    @api.response(201, 'Bucket List successfully created')
    @api.expect(bucket_list)
    def post(self):
        '''
        This creates an individual bucket list
        '''
        data = jsonify.request()
        create_bucket_list(data)
        return None, 201
