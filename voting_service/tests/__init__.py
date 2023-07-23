# tests/__init__.py
import unittest
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zombi:C0mpradors*@localhost/voting_service_db_test'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
