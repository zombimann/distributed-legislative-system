# tests/test_routes.py

import unittest
from app import app, db
from app.models import Amendment

class TestAmendmentService(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_amendments_empty(self):
        response = self.app.get('/api/amendments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        response = self.app.post('/api/amendments', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "Amendment created successfully.")

        # Verify the amendment is created
        response = self.app.get('/api/amendments/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["title"], "Amendment 1")
        self.assertEqual(response.json["description"], "Description of Amendment 1")
        self.assertEqual(response.json["proposed_by"], "User1")

    def test_get_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        self.app.post('/api/amendments', json=data)

        response = self.app.get('/api/amendments/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["title"], "Amendment 1")
        self.assertEqual(response.json["description"], "Description of Amendment 1")
        self.assertEqual(response.json["proposed_by"], "User1")

    def test_get_nonexistent_amendment(self):
        response = self.app.get('/api/amendments/999')  # Use a non-existent ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Amendment not found."})

    def test_edit_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        self.app.post('/api/amendments', json=data)

        data = {"title": "Amendment 1 - Updated", "description": "Updated description of Amendment 1"}
        response = self.app.put('/api/amendments/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Amendment updated successfully.")

        # Verify the updated data
        response = self.app.get('/api/amendments/1')
        self.assertEqual(response.json["title"], "Amendment 1 - Updated")
        self.assertEqual(response.json["description"], "Updated description of Amendment 1")
        self.assertEqual(response.json["proposed_by"], "User1")

    def test_edit_nonexistent_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        self.app.post('/api/amendments', json=data)

        data = {"title": "Amendment 1 - Updated", "description": "Updated description of Amendment 1"}
        response = self.app.put('/api/amendments/999', json=data)  # Use a non-existent ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Amendment not found."})

    def test_delete_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        self.app.post('/api/amendments', json=data)

        response = self.app.delete('/api/amendments/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Amendment deleted successfully.")

        # Verify the amendment is deleted
        response = self.app.get('/api/amendments/1')
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_amendment(self):
        data = {"title": "Amendment 1", "description": "Description of Amendment 1", "proposed_by": "User1"}
        self.app.post('/api/amendments', json=data)

        response = self.app.delete('/api/amendments/999')  # Use a non-existent ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "Amendment not found."})

if __name__ == '__main__':
    unittest.main()
