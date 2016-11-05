from flask_restplus import abort, Resource
from app.blister_api.serializer import user
from app import api


ns = api.namespace(
    'auth/register',
    description="Operations related to individual user registeration.")


@ns.route('/')
@api.response(200, 'Success')
class RegisteUser(Resource):
    def post(self):
        return {'username':'kimani'}
