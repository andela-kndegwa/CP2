from flask import request
from flask_restplus import abort, Resource
from app import api
from app.blister_api.serializer import bucket_list_item
from app.blister_api.models import BucketListItem
from app.blister_api.actions import create_bucket_list_item


ns = api.namespace(
    'blister/bucket_list_items',
    description="Operations related to bucket lists items.")


@ns.route('/')
class BucketListCollection(Resource):
    """
    This method retrieves all the bucket lists associcated
    with a particular user.
    """
    @api.marshal_with(bucket_list_item)
    def get(self):
        '''
        This shows a list of all the bucket list items on blister.
        '''
        bucket_lists = BucketListItem.query.all()
        if not bucket_lists:
            abort(404, message='There are no bucket list items at the moment.')
        else:
            return bucket_lists

    @api.response(201, 'Bucket List Item successfully created.')
    @api.expect(bucket_list_item)
    def post(self):
        """
        Creates a new bucket list item category.
        """
        data = request.json
        create_bucket_list_item(data)
        return data, 201
