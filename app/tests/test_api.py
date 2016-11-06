import json
from flask_testing import TestCase
from app import create_app, db, api
from app.blister_api.models import User, BucketList, BucketListItem
from app.blister_api.endpoints.bucket_lists import BucketListCollection
from app.blister_api.endpoints.items import BucketListItemCollection
# from app.blister_api.endpoints.register_user import ns as register_namespace
# from app.blister_api.endpoints.login_user import ns as login_namespace

import base_setup


base_url = '/api/v1.0/'


class TestEndpointsClass(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.blister = self.create_app().test_client()
        db.create_all()
        api.add_resource(BucketListCollection, base_url + 'bucketlists')
        api.add_resource(BucketListItemCollection,
                         base_url + 'bucketlists/items')

    def test_home_returns_404(self):
        '''
                Return 404 because the route is not
                set in application.

                change this to welcome to the api.
        '''
        response = self.blister.get('/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_home_blueprint_message(self):
        '''
                Return Ok because
                the resource has been moved by the flask
                blueprint to api/v1.0/
        '''
        response = self.blister.get(base_url)
        self.assertEqual(response.status_code, 200)

    def test_bucket_list_route(self):
        '''
        RERTURN MESSAGE TO SHWO THE URL WSA ACTUALLY FOUND.
        STATUS 200
        '''
        response = self.blister.get(base_url + 'bucketlists/')
        self.assertEqual(response.data, 'There are no bucket lists as of now.')
        self.assertEqual(response.status_code, 200)

    def test_bucket_list_item_route(self):
        response = self.blister.get(base_url + '/bucketlists/items')
        self.assertIn('There are no bucket list items at the moment',
                      response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)

    # def test_post_bucket_list(self):
    #     credentials = {'username': 'mrkimani', 'password':'pass'}
    #     self.blister.post(base_url + 'bucket_list/', data = json.dumps(credentials))

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAuthentication(TestCase):

    def create_app(self):
        return create_app('testing')

    # def setUp(self):
    #     db.create_all()
    #     api.add_namespace(register_namespace)
    #     api.add_namespace(login_namespace)
    #     db.create_all()
    #     self.body = {
    #         "username": "alexmagana",
    #         "password": "safari",
    #     }
    #     self.test_client = self.create_app().test_client()
    #     self.response = base_setup.send_post(self.test_client, base_url + '/auth/register',
    #                                          self.body)

    # def test_create_user_works(self):
    #     response_json = json.loads(self.response.data.decode('utf-8'))
    #     self.assertEqual(self.response.status_code, 201)
    #     self.assertIn('token', response_json)

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
