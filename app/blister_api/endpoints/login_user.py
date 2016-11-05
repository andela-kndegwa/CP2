from flask_restplus import abort, Resource
from app.blister_api.serializer import user
from app import api


ns = api.namespace(
    'auth/login',
    description="Operations related to individual user login.")


@ns.route('/')
@api.response(200, 'Success')
class LoginUser(Resource):
    def post(self):
        pass
