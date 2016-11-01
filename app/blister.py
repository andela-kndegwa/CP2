from app import create_app, api
from flask_restplus import Resource
from blister_api.endpoints.bucket_lists import ns as bucket_lists_namespace
from blister_api.endpoints.items import ns as items_namespace
from blister_api.endpoints.users import ns as users_namespace
# from app import create_app
app = create_app('development')


# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         """
#                 this is a very interesting ui
#         """
#         return {'hello': 'world'}


api.add_namespace(bucket_lists_namespace)
api.add_namespace(items_namespace)
api.add_namespace(users_namespace)


if __name__ == '__main__':
    app.run()
