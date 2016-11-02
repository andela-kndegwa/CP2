# import factory  # imports the faactory boy module.
# import models
import unittest  # Python unittesting framework
from flask_testing import TestCase
from app import create_app, db


class TestBlisterModelFunctionality(TestCase):
    """
    This allows us to Test our models functionalty.


    Factory is used to create random and Faker
    classes that can be utilised during our tests and discarded
    after.
    """

    def create_app(self, config_name='testing'):

        # pass in test configuration
        a = create_app(config_name)
        return a

    def setUp(self):
        db.create_all()

    def test_testing_database_created(self):
        app = create_app('testing')
        self.assertTrue(app.config['TESTING'])

    def test_name_database_created(self):
        app = create_app('testing')
        self.assertEqual(app.config['db_name'], 'blister-test.sqlite')

    def tearDown(self):

        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
