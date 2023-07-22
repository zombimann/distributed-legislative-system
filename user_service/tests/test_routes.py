#app/test_routes.py


from tests import BaseTestCase
import unittest
import json
from app import create_app, db
from app.models import User

class UserRoutesTestCase(BaseTestCase):
    def test_user_registration(self):
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
        response = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        data = {
            "username": "test_user",
            "password": "test_password"
        }
        response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile_unauthenticated(self):
        response = self.client.get('/api/profile')
        self.assertEqual(response.status_code, 401)

    def test_get_user_profile_authenticated(self):
        # Register a test user
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
        self.client.post('/api/register', data=json.dumps(data), content_type='application/json')

        # Login the test user
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        login_response = self.client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(login_response.status_code, 200)

        # Extract JWT access token from login response
        access_token = login_response.get_json()['access_token']
        headers = {"Authorization": f"Bearer {access_token}"}

        # Get user profile with authentication
        response = self.client.get('/api/profile', headers=headers)
        self.assertEqual(response.status_code, 200)

        # Check if the retrieved profile matches the registered user
        profile_data = response.get_json()
        self.assertEqual(profile_data['username'], "test_user")
        self.assertEqual(profile_data['email'], "test@example.com")

    def test_invalid_username_login(self):
        data = {
            "username": "non_existent_user",
            "password": "test_password"
        }
        response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_invalid_password_login(self):
        data = {
            "username": "test_user",
            "password": "incorrect_password"
        }
        response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_empty_fields_registration(self):
        data = {
            "username": "",
            "email": "",
            "password": ""
        }
        response = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_empty_fields_login(self):
        data = {
            "username": "",
            "password": ""
        }
        response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_duplicate_username_registration(self):
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
        response1 = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response2.status_code, 409)

    def test_get_user_profile_not_found(self):
        # Get user profile with an invalid JWT token (non-existent user)
        headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get('/api/profile', headers=headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
