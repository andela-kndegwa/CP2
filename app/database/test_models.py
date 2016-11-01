import factory  # imports the faactory boy module.
import models
import unittest  # Python unittesting framework
from app.config import config


class TestBlisterModelFunctionality(unittest.TestCase):
    """
    This allows us to Test our models functionalty.


    Factory is used to create radndom and Faker
    classes that can be utilised during our tests and discarded
    after.
    """

    def setUp(self):
        class UserFactory(factory.Factory):
            """docstring for UserFactory"""
            class Meta:
                model = models.User
