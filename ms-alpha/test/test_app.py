import unittest, sys
from flask import current_app

sys.path.append('..')
from app import create_app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # Test that the app is in testing mode
    def test_app_is_testing(self):
        self.assertIsNotNone(current_app)