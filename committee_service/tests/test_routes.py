#tests/test_routes.py

import unittest
import json
from app.routes import committee_routes, db
from app.models import CommitteeMember

class TestCommitteeRoutes(unittest.TestCase):
    def setUp(self):
        committee_routes.config['ENV'] = 'testing'
        committee_routes.config['DEBUG'] = False
        committee_routes.config['TESTING'] = True
        self.app = committee_routes.test_client()
        with committee_routes.app_context():
            db.create_all()

    def tearDown(self):
        with committee_routes.app_context():
            db.drop_all()

    def test_nominate_candidate(self):
        response = self.app.post('/api/committee/nominate', data=json.dumps({'name': 'John Doe'}), content_type='application/json')
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Candidate nominated successfully.')

    def test_nominate_duplicate_candidate(self):
        self.app.post('/api/committee/nominate', data=json.dumps({'name': 'John Doe'}), content_type='application/json')
        response = self.app.post('/api/committee/nominate', data=json.dumps({'name': 'John Doe'}), content_type='application/json')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Candidate is already nominated.')

    def test_get_committee_members(self):
        # Nominate a candidate
        self.app.post('/api/committee/nominate', data=json.dumps({'name': 'John Doe'}), content_type='application/json')

        # Get the committee members (expecting 0 initially)
        with committee_routes.app_context():
            response = self.app.get('/api/committee/members')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 0)

        # Elect the nominated candidate
        with committee_routes.app_context():
            candidate = CommitteeMember.query.filter_by(name='John Doe').first()
            candidate.elected_status = True
            db.session.commit()

        # Get the committee members again (expecting 1 now)
        with committee_routes.app_context():
            response = self.app.get('/api/committee/members')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['name'], 'John Doe')

    def test_nominate_candidate_without_name(self):
        response = self.app.post('/api/committee/nominate', data=json.dumps({}), content_type='application/json')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Please provide a valid name.')
