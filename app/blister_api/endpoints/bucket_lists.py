from flask import request
from flask_restplus import abort, Resource
from app import api
from app.blister_api.serializer import bucket_list_item, bucket_list
from app.blister_api.models import BucketList
from app.blister_api.actions import create_bucket_list


ns = api.namespace(
    'blister/bucket_lists',
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
            abort(404, message='There are no bucket lists at the moment.')
        else:
            return bucket_lists

