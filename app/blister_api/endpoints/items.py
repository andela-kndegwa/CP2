from flask import request, jsonify
from flask_restplus import abort, Resource
from app import api
# from app.blister_api.serializer import bucket_list_item
from app.blister_api.models import BucketListItem
from app.blister_api.actions import create_bucket_list_item


# ns = api.namespace(
#     'bucketlists/items/',
#     description="Operations related to bucket lists items.")


class BucketListItemCollection(Resource):
    """
    This method retrieves all the bucket lists associcated
    with a particular user.
    """
    def get(self):
        '''
        This shows a list of all the bucket list items on blister.
        '''
        bucket_lists = BucketListItem.query.all()
        if not bucket_lists:
            message = 'There are not bucket lists as of now'
            return jsonify(message)
        else:
            return bucket_lists

    def post(self):
        """
        Creates a new bucket list item category.
        """
        data = request.json
        create_bucket_list_item(data)
        return data, 201
