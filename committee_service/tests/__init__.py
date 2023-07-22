#tests/__init__.py

import unittest
from app import app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_pyfile('../config.py')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
