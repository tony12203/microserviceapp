import unittest
import json
from app import app, db, User

class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and create the database tables."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create database tables

    def tearDown(self):
        """Remove the test database after each test."""
        with self.app.app_context():
            db.drop_all()  # Cleanup test database

    def test_add_user(self):
        """Test adding a new user."""
        response = self.client.post('/users', data=json.dumps({
            'name': 'John Doe',
            'email': 'john@example.com'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))

        response2 = self.client.get('/users')
        self.assertEqual(json.loads(response2.data)[0]['name'], 'John Doe')

    def test_get_users(self):
        """Test getting all users."""
        self.client.post('/users', data=json.dumps({
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        }), content_type='application/json')

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        users = json.loads(response.data)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], 'Jane Doe')

    def test_update_user(self):
        """Test updating an existing user."""
        response = self.client.post('/users', data=json.dumps({
            'name': 'Alice',
            'email': 'alice@example.com'
        }), content_type='application/json')

        user_id = json.loads(response.data)['id']
        response = self.client.put(f'/users/{user_id}', data=json.dumps({
            'name': 'Alice Updated',
            'email': 'alice_updated@example.com'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

        response2 = self.client.get('/users')
        self.assertEqual(json.loads(response2.data)[0]['name'], 'Alice Updated')

    def test_delete_user(self):
        """Test deleting a user."""
        response = self.client.post('/users', data=json.dumps({
            'name': 'Bob',
            'email': 'bob@example.com'
        }), content_type='application/json')

        user_id = json.loads(response.data)['id']
        response = self.client.delete(f'/users/{user_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

        response2 = self.client.get('/users')
        self.assertEqual(response2.json, [])

if __name__ == '__main__':
    unittest.main()