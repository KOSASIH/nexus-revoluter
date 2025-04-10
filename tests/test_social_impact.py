# test_social_impact.py

import unittest
import json
from app import app, db, User, Project  # Adjust the import based on your project structure

class SocialImpactTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client and the test database
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_social_impact.db'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User  registered successfully', response.data)

    def test_login_user(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_create_project(self):
        # First, register and log in the user
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = json.loads(login_response.data)['access_token']

        # Create a project
        response = self.client.post('/projects', json={
            'title': 'Community Garden',
            'description': 'A garden for the community to grow vegetables.',
            'goal_amount': 1000
        }, headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Project created successfully', response.data)

    def test_donate_to_project(self):
        # Register and log in the user
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = json.loads(login_response.data)['access_token']

        # Create a project
        self.client.post('/projects', json={
            'title': 'Community Garden',
            'description': 'A garden for the community to grow vegetables.',
            'goal_amount': 1000
        }, headers={'Authorization': f'Bearer {access_token}'})

        # Get the project ID
        project = Project.query.first()

        # Donate to the project
        response = self.client.post(f'/donate/{project.id}', json={
            'amount': 100,
            'source': 'tok_visa'  # Use a valid Stripe token for testing
        }, headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Donation successful', response.data)

    def test_get_projects(self):
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_project_details(self):
        # Register and log in the user
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = json.loads(login_response.data)['access_token']

        # Create a project
        self.client.post('/projects', json={
            'title': 'Community Garden',
            'description': 'A garden for the community to grow vegetables.',
            'goal_amount': 1000
        }, headers={'Authorization': f'Bearer {access_token}'})

        # Get the project ID
        project = Project.query.first()

        # Get project details
        response = self.client.get(f'/projects/{project.id}')
        self.assertEqual (response.status_code, 200)
        self.assertIn(b'Community Garden', response.data)

if __name__ == '__main__':
    unittest.main()
