# tests/test_routes.py

import unittest
from flask import Flask
from app import create_app, db
from app.models import Bill

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.test_request_context()  # Create the app context within setUp
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Pop the app context within tearDown

    def test_create_bill(self):
        data = {'title': 'Test Bill', 'description': 'Test description', 'author': 'Test Author'}
        response = self.app.post('/api/bills', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Bill created successfully'})

    def test_get_bills_empty(self):
        response = self.app.get('/api/bills')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_bills_non_empty(self):
        bill1 = Bill(title='Bill 1', description='Description 1', author='Author 1')
        bill2 = Bill(title='Bill 2', description='Description 2', author='Author 2')

        with self.app_context:
            db.session.add(bill1)
            db.session.add(bill2)
            db.session.commit()

        response = self.app.get('/api/bills')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_edit_bill(self):
        bill = Bill(title='Test Bill', description='Test description', author='Test Author')
        with self.app_context:
            db.session.add(bill)
            db.session.commit()

        data = {'title': 'Updated Title', 'description': 'Updated description'}
        response = self.app.put(f'/api/bills/{bill.id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Bill updated successfully'})

    def test_vote_on_bill(self):
        bill = Bill(title='Test Bill', description='Test description', author='Test Author')
        with self.app_context:
            db.session.add(bill)
            db.session.commit()

        data = {'user_id': 1, 'vote': True}

        # First vote
        response1 = self.app.post(f'/api/bills/{bill.id}/vote', json=data)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.get_json(), {'message': 'Vote recorded successfully'})

        # Second vote
        response2 = self.app.post(f'/api/bills/{bill.id}/vote', json=data)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.get_json(), {'message': 'User already voted on this bill'})

    def test_vote_on_nonexistent_bill(self):
        data = {'user_id': 1, 'vote': True}
        response = self.app.post('/api/bills/1000/vote', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'message': 'Bill not found'})

    def test_vote_with_invalid_data(self):
        bill = Bill(title='Test Bill', description='Test description', author='Test Author')
        with self.app_context:
            db.session.add(bill)
            db.session.commit()

        data1 = {'user_id': 1}  # Missing 'vote' field
        response1 = self.app.post(f'/api/bills/{bill.id}/vote', json=data1)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.get_json(), {'message': 'Vote value is required'})

        data2 = {'user_id': 1, 'vote': True}  # Valid 'vote' value (True)
        response2 = self.app.post(f'/api/bills/{bill.id}/vote', json=data2)
        self.assertIn(response2.status_code, [200, 201])
        self.assertEqual(response2.get_json(), {'message': 'Vote recorded successfully'})

        # data3 = {'user_id': 1, 'vote': False}  # Valid 'vote' value (False)
        # response3 = self.app.post(f'/api/bills/{bill.id}/vote', json=data3)
        # self.assertIn(response3.status_code, [200, 201])
        # self.assertEqual(response3.get_json(), {'message': 'Vote recorded successfully'})

        # data4 = {'user_id': 1, 'vote': 'Invalid'}  # Invalid 'vote' value
        # response4 = self.app.post(f'/api/bills/{bill.id}/vote', json=data4)
        # self.assertEqual(response4.status_code, 400)
        # self.assertEqual(response4.get_json(), {'message': 'Invalid vote value'})

        # data5 = {'user_id': 'Invalid', 'vote': True}  # Invalid 'user_id' value
        # response5 = self.app.post(f'/api/bills/{bill.id}/vote', json=data5)
        # self.assertEqual(response5.status_code, 400)
        # self.assertEqual(response5.get_json(), {'message': 'Invalid user_id value'})

        # data6 = {'user_id': -1, 'vote': True}  # Invalid 'user_id' value
        # response6 = self.app.post(f'/api/bills/{bill.id}/vote', json=data6)
        # self.assertEqual(response6.status_code, 400)
        # self.assertEqual(response6.get_json(), {'message': 'Invalid user_id value'})


if __name__ == '__main__':
    unittest.main()
