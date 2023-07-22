import json
import jwt
from datetime import datetime, timedelta
from tests import BaseTestCase
from app.models import Bill
from app import app, db

def generate_jwt_token(user_id):
    secret_key = app.config['SECRET_KEY']
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

class TestBillService(BaseTestCase):
    def test_create_bill(self):
        # Generate a JWT token for user with id=1
        token = generate_jwt_token(1)

        data = {
            "title": "Test Bill",
            "description": "This is a test bill.",
            "tags": "test, demo",
            "author_id": 1
        }
        response = self.client.post('/api/bills', data=json.dumps(data), content_type='application/json',
                                    headers={'Authorization': f'Bearer {token}'})
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Bill created successfully.')
        self.assertEqual(Bill.query.count(), 1)
        self.assertEqual(Bill.query.first().title, "Test Bill")

    def test_get_all_bills(self):
        # Generate JWT tokens for two users with ids 1 and 2
        token_user1 = generate_jwt_token(1)
        token_user2 = generate_jwt_token(2)

        # Create test bills for both users
        data1 = {
            "title": "Test Bill 1",
            "description": "This is a test bill 1.",
            "tags": "test, demo",
            "author_id": 1
        }
        data2 = {
            "title": "Test Bill 2",
            "description": "This is a test bill 2.",
            "tags": "test, demo",
            "author_id": 2
        }
        self.client.post('/api/bills', data=json.dumps(data1), content_type='application/json',
                         headers={'Authorization': f'Bearer {token_user1}'})
        self.client.post('/api/bills', data=json.dumps(data2), content_type='application/json',
                         headers={'Authorization': f'Bearer {token_user2}'})

        response = self.client.get('/api/bills')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_get_bill_details(self):
        # Generate a JWT token for user with id=1
        token = generate_jwt_token(1)

        # Create a test bill
        data = {
            "title": "Test Bill",
            "description": "This is a test bill.",
            "tags": "test, demo",
            "author_id": 1
        }
        self.client.post('/api/bills', data=json.dumps(data), content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'})

        # Get the bill details
        response = self.client.get('/api/bills/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], "Test Bill")
        self.assertEqual(data['description'], "This is a test bill.")
        self.assertEqual(data['tags'], "test, demo")
        self.assertEqual(data['author_id'], 1)

    def test_edit_bill(self):
        # Generate a JWT token for user with id=1
        token = generate_jwt_token(1)

        # Create a test bill
        data = {
            "title": "Test Bill",
            "description": "This is a test bill.",
            "tags": "test, demo",
            "author_id": 1
        }
        self.client.post('/api/bills', data=json.dumps(data), content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'})

        # Edit the bill
        updated_data = {
            "title": "Updated Test Bill",
            "description": "This is an updated test bill.",
            "tags": "updated, demo",
            "author_id": 1
        }
        response = self.client.put('/api/bills/1/edit', data=json.dumps(updated_data), content_type='application/json',
                                   headers={'Authorization': f'Bearer {token}'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Bill updated successfully.')

        # Get the updated bill details
        response = self.client.get('/api/bills/1')
        data = response.get_json()
        self.assertEqual(data['title'], "Updated Test Bill")
        self.assertEqual(data['description'], "This is an updated test bill.")
        self.assertEqual(data['tags'], "updated, demo")
        self.assertEqual(data['author_id'], 1)
