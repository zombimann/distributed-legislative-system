# tests/__init__.py
import unittest

from flask_testing import TestCase
from app import app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
