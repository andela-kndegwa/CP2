import simplejson
import json
from flask_testing import TestCase
from app import create_app, db, api
from app.blister_api.models import User, BucketList, BucketListItem
from app.blister_api.endpoints.bucket_lists import BucketListCollection
from app.blister_api.endpoints.items import BucketListItemCollection
from app.blister_api.endpoints.login import LoginUser
from app.blister_api.endpoints.register import RegisterUser, Home

# from app.blister_api.endpoints.register_user import ns as register_namespace
# from app.blister_api.endpoints.login_user import ns as login_namespace

import base_setup


base_url = '/api/v1.0'


class TestEndpointsClass(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.blister = self.create_app().test_client()
        db.create_all()
        api.add_resource(Home, '/', base_url)
        api.add_resource(RegisterUser, '/auth/register', endpoint='register')
        api.add_resource(LoginUser, '/auth/login', endpoint='login')
        api.add_resource(BucketListCollection,
                         '/bucketlists',
                         '/bucketlists/<int:id>',
                         '/bucketlists/<int:id>/',
                         endpoint='bucketlists')
        api.add_resource(BucketListItemCollection,
                         '/bucketlists/<int:bucketlist_id>/items',
                         '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
        self.body = {
            "username": "alexmagana",
            "password": "safari"
        }
        # self.test_client = self.create_app().test_client()
        # self.response = base_setup.send_post(self.test_client, base_url + '/auth/register/',
        #                                      self.body)

    def test_home_blueprint_message(self):
        '''
                Return 301 because
                the resource has been moved by the flask
                blueprint to api/v1.0/ and not api/v1.0
        '''
        response = self.blister.get(base_url)
        self.assertEqual(response.status_code, 301)
        self.assertIn('Redirect', response.data)

    def test_bucket_list_route(self):
        '''
        This method tests that indeed accessing the route when a user
        has not logged in is prohibited and indeed the app throws an
        unauthorized access error message.

        Returns:
        Response.data ---> Unauthorized Access
        Response.status_code --- > 401
        '''
        response = self.blister.get(base_url + '/bucketlists')
        self.assertEqual(
            response.data, 'Unauthorized Access')
        self.assertEqual(response.status_code, 401)

    # ======================================================
    # Tests user Login and Register functionality.
    def test_create_user_works(self):
        '''
        Arguments:
        Self---> itsa class method

        Returns:
        201 As it is a post request.
        '''
        url = base_url + '/auth/register'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('Sign Up successful.', response.data.decode('utf-8'))

    def test_username_and_password_required_to_register(self):
        self.body = {}
        self.body['username'] = ''
        self.body['password'] = 'pass'
        url = base_url + '/auth/register'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # self.assertIn('Please enter a username and password to register.', response.data.decode('utf-8'))

        # response_json = json.loads(self.response.data.decode('utf-8'))
        # self.assertEqual(self.response.status_code, 400)
        # self.assertIn('message', response_json)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


# class TestAuthentication(TestCase):

#     def create_app(self):
#         app = create_app('testing')
#         return app

#     def setUp(self):
#         db.create_all()
#         api.add_resource(Home, '/', base_url)
#         api.add_resource(RegisterUser, '/auth/register', endpoint='register')
#         api.add_resource(LoginUser, '/auth/login', endpoint='login')
#         api.add_resource(BucketListCollection,
#                          '/bucketlists',
#                          '/bucketlists/<int:id>',
#                          '/bucketlists/<int:id>/',
#                          endpoint='bucketlists')
#         api.add_resource(BucketListItemCollection,
#                          '/bucketlists/<int:bucketlist_id>/items',
#                          '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')

#         self.body = {"username": "alexmagana",
#                      "password": "safari"}
#         self.test_client = self.create_app().test_client()
#         self.response = base_setup.send_post(self.test_client, base_url + '/auth/register',
#                                              self.body)
#         # print(self.response.headers)
#         # print(self.response.json)
#         print(self.response.data)

#     def test_create_user_works(self):
#         url = base_url + '/auth/register'
#         response = self.test_client.post(url,
#                                          data=self.body)
#         print(response.headers)
#         # print(response.text)
#         print(response.data)
#         response_json = json.loads(response.data.decode('utf-8'))
#         self.assertEqual(self.response.status_code, 201)
#         self.assertIn('token', response_json)

    # def test_create_user_username_required(self):
    #     response_json = json.loads(self.response.data.decode('utf-8'))
    #     self.assertEqual(self.response.status_code, 400)
    #     self.assertIn('message', response_json)

    # def test_user_exist(self):
    #     second_response = base_setup.send_post(
    #         self.test_client, '/v1.0/auth/register', self.body)
    #     response_json = json.loads(second_response.data.decode('utf-8'))
    #     self.assertEqual(second_response.status_code, 400)

    # def test_login(self):
    #     response = base_setup.send_post(
    #         self.test_client, '/v1.0/auth/login', self.body)
    #     response_json = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('token', response_json)

    # def test_login_fail(self):
    #     body = {
    #         "username": "alexmagana",
    #         "password": "nothispassword"
    #     }
    #     response = base_setup.send_post(
    #         self.test_client, '/v1.0/auth/login', body)
    #     self.assertEqual(response.status_code, 400)
