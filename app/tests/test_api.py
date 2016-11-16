import json
from flask_testing import TestCase

from app import create_app, db, api
from app.blister_api.endpoints.bucket_lists import (BucketListCollection,
                                                    SingleBucketList)
from app.blister_api.endpoints.items import (BucketListItemCollection,
                                             SingleBucketListItem)
from app.blister_api.endpoints.login import LoginUser
from app.blister_api.endpoints.register import RegisterUser, Home


def authorization_header(token):
    headers = {
        'Authorization': 'Bearer ' + token
    }
    return headers


base_url = '/api/v1.0'


class TestEndpointsClass(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        self.blister = self.create_app().test_client()
        db.create_all()
        api.add_resource(Home, '/', 'api/v1.0', endpoint='home')
        api.add_resource(RegisterUser, '/auth/register', endpoint='register')
        api.add_resource(LoginUser, '/auth/login', endpoint='login')

        api.add_resource(BucketListCollection, '/bucketlists',
                         endpoint='bucketlists')
        api.add_resource(SingleBucketList, '/bucketlists/<int:id>')

        api.add_resource(BucketListItemCollection,
                         '/bucketlists/<int:bucketlist_id>/items')

        api.add_resource(SingleBucketListItem,
                         '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
        self.body = {
            "username": "alexmagana",
            "password": "safari"
        }
        url = base_url + '/auth/register'
        self.response = self.blister.post(url, data=json.dumps(self.body),
                                          content_type="application/json")

        login_url = base_url + '/auth/login'
        self.login_response = self.blister.post(login_url, data=json.dumps(self.body),
                                                content_type="application/json")
        # Login credentials
        self.response_json = json.loads(
            self.login_response.data.decode('utf-8'))
        self.token = self.response_json['token']
        self.headers = authorization_header(self.token)

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
    def test_username_and_password_required_to_register(self):
        self.body = {}
        self.body['username'] = ''
        self.body['password'] = ''
        url = base_url + '/auth/register'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a username and password to register.',
                      response.data.decode('utf-8'))

    def test_register_user_works(self):
        '''
        Arguments:
        Self---> is a class method

        Returns:
        201 As it is a post request.

        It is tied to the self.response that relates to this
        class because a user should be able to register with
        the self.body credentials.
        '''
        self.assertEqual(self.response.status_code, 201)
        self.assertIn('Sign Up successful.',
                      self.response.data.decode('utf-8'))

    def test_username_and_password_required_to_login(self):
        self.body = {}
        self.body['username'] = ''
        self.body['password'] = ''
        url = base_url + '/auth/login'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a username and password to log in.',
                      response.data.decode('utf-8'))

    def test_invalid_credentials_are_caught_works(self):
        '''
        Arguments:
        Self---> It is a class method

        Returns:
        401 As it is an unauthorized access request
        '''
        self.body = {}
        self.body['username'] = 'alexmagana'
        self.body['password'] = 'wrongpassword'
        url = base_url + '/auth/login'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            'Authentication failed. Invalid login credentials.',
            response.data.decode('utf-8'))

    def test_login_works(self):
        '''
        Arguments:
        Self---> It is a class method

        Returns:
        201 As it is a post request.
        '''
        url = base_url + '/auth/login'
        response = self.blister.post(url, data=json.dumps(self.body),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data.decode('utf-8'))
    # ======================================================
    # Tests Buckelist Resource functionality.

    def test_get_when_there_are_no_bucketlists(self):
        url = base_url + '/bucketlists'
        response = self.blister.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Perform at the grammies',
            'description': 'Joel Ortiz'
        }
        response = self.blister.post(url, headers=self.headers,
                                     data=json.dumps(body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Joel Ortiz', response.data.decode('utf-8'))

    def test_create_bucketlist_with_same_title(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Perform at the grammies',
            'description': 'Joel Ortiz'
        }
        self.blister.post(url, headers=self.headers,
                          data=json.dumps(body),
                          content_type='application/json')

        body = {
            'title': 'Perform at the grammies',
            'description': 'Khaligraph Jones'
        }

        response = self.blister.post(url, headers=self.headers,
                                     data=json.dumps(body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Two bucket lists cannot have the same title.',
                      response.data.decode('utf-8'))

    def test_update_bucketlist(self):
        post_url = base_url + '/bucketlists'
        post_body = {
            'title': 'Perform at the grammies',
            'description': 'Joel Ortiz'
        }
        response = self.blister.post(post_url, headers=self.headers,
                                     data=json.dumps(post_body),
                                     content_type='application/json')
        put_url = base_url + '/bucketlists/1'
        put_body = {
            'description': 'Kendrick Lamar'
        }
        response = self.blister.put(put_url, headers=self.headers,
                                    data=json.dumps(put_body),
                                    content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        self.assertNotIn('Joel Ortiz', response.data.decode('utf-8'))
        self.assertIn('Kendrick Lamar', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        post_url = base_url + '/bucketlists'
        post_body = {
            'title': 'Perform at the grammies',
            'description': 'Joel Ortiz'
        }
        response = self.blister.post(post_url, headers=self.headers,
                                     data=json.dumps(post_body),
                                     content_type='application/json')
        delete_url = base_url + '/bucketlists/1'
        response = self.blister.delete(delete_url, headers=self.headers,
                                       content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, '')
    # ======================================================
    # Tests Buckelist Item Resource functionality.

    def test_message_when_no_items_in_bucketlist(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Tomorrow Land',
            'description': 'Kick it with them Ninjas down the block.'
        }
        response = self.blister.post(url, headers=self.headers,
                                     data=json.dumps(body),
                                     content_type='application/json')
        get_items_url = url + '/1/items'
        response = self.blister.get(get_items_url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist_item(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Tomorrow Land',
            'description': 'Kick it with them Ninjas down the block.'
        }
        self.blister.post(url, headers=self.headers,
                          data=json.dumps(body),
                          content_type='application/json')
        post_item_url = url + '/1/items'
        item_body = {
            'title': 'Dance with the stars',
            'description': 'Tiesto bumping that loud'
        }

        response = self.blister.post(post_item_url, headers=self.headers,
                                     data=json.dumps(item_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Dance with the stars', response.data.decode('utf-8'))

    def test_create_bucketlist_item_with_no_data(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Today Land',
            'description': 'Kick it with them Ninjas down the block.'
        }
        self.blister.post(url, headers=self.headers,
                          data=json.dumps(body),
                          content_type='application/json')
        post_item_url = url + '/1/items'
        item_body = {}
        response = self.blister.post(post_item_url, headers=self.headers,
                                     data=json.dumps(item_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_bucketlist_item(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Jump of a cliff',
            'description': 'With a strap attached offcourse!'
        }
        self.blister.post(url, headers=self.headers,
                          data=json.dumps(body),
                          content_type='application/json')
        post_item_url = url + '/1/items'
        item_body = {
            'title': 'Himalayas',
            'description': 'Like a boss'
        }

        self.blister.post(post_item_url, headers=self.headers,
                          data=json.dumps(item_body),
                          content_type='application/json')

        put_item_url = url + '/1/items/1'
        put_body = {
            'description': 'Unlike Rick Ross'
        }
        response = self.blister.put(put_item_url, headers=self.headers,
                                    data=json.dumps(put_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Like a boss', response.data.decode('utf-8'))

    def test_delete_bucketlist_item(self):
        url = base_url + '/bucketlists'
        body = {
            'title': 'Will work with Wale',
            'description': 'DC All day. NO days off.'
        }
        self.blister.post(url, headers=self.headers,
                          data=json.dumps(body),
                          content_type='application/json')
        post_item_url = url + '/1/items'
        item_body = {
            'title': 'L.A Studios DC',
            'description': 'Have some good times.'
        }

        self.blister.post(post_item_url, headers=self.headers,
                          data=json.dumps(item_body),
                          content_type='application/json')

        delete_item_url = url + '/1/items/1'
        response = self.blister.delete(delete_item_url, headers=self.headers,
                                       content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, '')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
