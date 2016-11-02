from flask_restplus import Resource
from app import api


ns = api.namespace(
    'blister/bucket_lists', description="Options related to individual bucket lists.")


@ns.route('/')
class CategoryCollection(Resource):
    def get(self):
        """
        This method retrieves all the bucket lists associcated
        with a particular user.
        """
        return {'hello': 'world'}
