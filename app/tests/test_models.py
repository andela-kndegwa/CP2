from app.blister_api.models import User, BucketListItem, BucketList
import unittest  # Python unittesting framework
from app import create_app, db
import time


class TestUserModelFunctionality(unittest.TestCase):
    """
    This allows us to Test User Model functionalty.

    """

    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        db.create_all()
        self.user = User(username="mrkimani", password="pass")
        db.session.add(self.user)
        db.session.commit()
        self.auth_token = self.user.generate_authentication_token()

    def test_database_created_is_valid(self):
        """
        This ensures the right configurations
        are configured for the database.

        Expectation:
        The test should assert to True.
        """
        self.assertTrue(self.app.config['TESTING'])

    def test_creates_user_with_right_properties(self):
        '''
        The user created should have an id of 1
        '''
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.username, 'mrkimani')

    def test_password_verification_works(self):
        '''
        After hashing the password, the user credentials
        should not change.
        '''
        self.assertFalse(self.user.verify_password('password'))
        self.assertTrue(self.user.verify_password('pass'))

    def test_generate_authentication_token(self):
        """
        Test it returns a dictionary with id and a
        generated token as the value.
        """
        self.assertIsNotNone(self.auth_token)

    def test_query_user_from_test_database_if_invalid_password(self):
        """
        Arguments:
        username, password

        Returns:
        Error Message ---> Incorrect password
        """
        res = User.query_user('mrkimani', 'password')
        self.assertEquals(res, 'Authentication failed. Invalid login credentials.')

    def test_verification_token_expiry(self):
        """
        Possible Outcomes:
        None ---> if BadSignature
        None ---> if SignatureExpired
        OK ---> if within time
        """
        app_token = self.user.generate_authentication_token(expires_in=0.3)
        time.sleep(1)
        self.assertEquals(self.user.verify_auth_token(app_token), 'Valid BUT expired token returned.')

    def test_query_user_from_test_database_if_user_non_existent(self):
        """
        Arguments:
        username, password

        Returns:
        Error Message ---> User does not exist
        """
        res = User.query_user('mrskimani', 'password')
        self.assertEquals(res, 'Authentication failed. User does not exist.')

    def test_query_user_from_test_database_if_details_ok(self):
        """
        Arguments:
        username, password

        Returns:
        Gets user

        Use case:
        This is most likely going to be the method
        that logs a user in to the API.
        """
        res = User.query_user('mrkimani', 'pass')
        self.assertIsNotNone(res)

    def test_invalid_token(self):
        """
        This ensures only the SECRET_KET stored
        in the app.config['SECRET_KEY'] variable can
        be used to create a token. Anything else is
        rejected.
        """
        fake_key = 'ANY_THING_APART_FROM_THE_SECRET_KEY'
        self.assertEquals(User.verify_auth_token(fake_key), 'Bad Signature on token.')

    def tearDown(self):
        db.drop_all()


class TestBucketListModelFunctionality(unittest.TestCase):
    """
    This allows us to Test User Model functionalty.

    """

    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        db.create_all()
        title = "Perform at the Grammys"
        self.bucketlist = BucketList(title=title, user_id=1)
        db.session.add(self.bucketlist)
        db.session.commit()

    def test_creates_bucket_list_with_right_properties(self):
        '''
        The bucket_list created should have an id of 1
        and the other title as a property.
        '''
        self.assertEqual(self.bucketlist.id, 1)
        self.assertNotEqual(self.bucketlist.title, 'Perform at the Oscars')
        self.assertEqual(self.bucketlist.title, 'Perform at the Grammys')

    def test_returns_message_if_bucket_list_does_not_exist(self):
        """
        Arguments:
        Bucket List title

        Returns:
        Error Message ---> Bucket List does not exist
        """
        res = BucketList.query_bucket_list('Perform at Kisumu Night')
        self.assertEquals(res, 'Bucket list does not exist')

    def test_returns_message_if_bucket_list_exists(self):
        """
        Arguments:
        Bucket List title

        Returns:
        user
        """
        res = BucketList.query_bucket_list('Perform at the Grammys')
        self.assertIsNotNone(res)

    def tearDown(self):
        db.drop_all()


class TestBucketListItemModelFunctionality(unittest.TestCase):
    """
    This allows us to Test User Model functionalty.

    """

    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        db.create_all()
        title = "Ohio 2017"
        description = "Jump jump"
        self.item = BucketListItem(
            title=title, description=description, bucketlist_id=1)
        db.session.add(self.item)
        db.session.commit()

    def test_creates_bucket_list_with_right_properties(self):
        '''
        The bucket_list item  created should have an id of 1
        and the other title as a property.
        '''
        self.assertEqual(self.item.id, 1)
        self.assertNotEqual(self.item.title, 'Ohio 2016')
        self.assertEqual(self.item.title, 'Ohio 2017')

    def test_returns_message_if_item_does_not_exist(self):
        """
        Arguments:
        Bucket List Item title

        Returns:
        Error Message ---> Bucket List Item does not exist
        """
        res = BucketListItem.query_item('Perform at Kisumu Night')
        self.assertEquals(res, 'Bucket list item does not exist')

    def test_returns_message_if_bucket_list_exists(self):
        """
        Arguments:
        Bucket List title

        Returns:
        user
        """
        res = BucketListItem.query_item('Ohio 2017')
        self.assertIsNotNone(res)

    def tearDown(self):
        db.drop_all()
