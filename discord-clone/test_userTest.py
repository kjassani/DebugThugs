import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from db import remove_room_members, save_user, get_user, users_collection, delete_user
from pymongo.errors import DuplicateKeyError
from main import app
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from unittest.mock import patch
from bson import ObjectId
from db import add_room_members

class UserTest(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        # Clean up any resources used for testing
        pass

    def test_generate_password_hash(self):
        password = 'password123'
        hashed_password = generate_password_hash(password)
        self.assertTrue(check_password_hash(hashed_password, password))

    def test_duplicate_user(self):
        delete_user('zain')
        save_user(username='zain',email='j@i.com', password='password123')
        with self.assertRaises(DuplicateKeyError):
            save_user(username='zain',email='j@i.com', password='password123')
            
    def test_get_userid(self):
        usern = get_user('zain')
        self.assertEqual(usern.get_id(), 'zain')
    def test_login(self):
        self.app.post('/login', data=dict(username='zain', password='password123'), follow_redirects=True)
    
    def test_signup(self):
        self.app.post('/signup', data=dict(username='jay', email = 'j@i.com',password = 'password123'), follow_redirects=True)

    def test_logout(self):
        self.app.get('/logout', follow_redirects=True)

    def test_create_room(self):
        self.app.post('/create-room', data=dict(room_name='room1'), follow_redirects=True)

    @patch('db.members_collection')
    def test_add_room_members(self, mock_members_collection):

        room_id = str(ObjectId())
        room_name = 'Test Room'
        usernames = ['user1', 'user2']
        added_by = 'admin'

        add_room_members(room_id, room_name, usernames, added_by)

        mock_members_collection.insert_many.assert_called_once_with(
            [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
            'is_room_admin': False} for username in usernames])

    @patch('db.members_collection')
    def test_remove_room_members(self, mock_members_collection):
        room_id = str(ObjectId())
        usernames = ['user1', 'user2']

        remove_room_members(room_id, usernames)

        
        mock_members_collection.delete_many.assert_called_once_with(
            {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


if __name__ == '__main__':
    unittest.main()