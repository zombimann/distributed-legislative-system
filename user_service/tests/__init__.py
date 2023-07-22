# tests/__init__.py

import os
import unittest
from app import create_app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test app
        self.app = create_app()
        self.app.config.from_pyfile('../config.py')
        self.client = self.app.test_client()

        # Set up the test database
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
