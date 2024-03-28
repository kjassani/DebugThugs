import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from db import remove_room_members, save_user, get_user, users_collection, delete_user, rooms_collection
from pymongo.errors import DuplicateKeyError
from main import app, create_room
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from unittest.mock import patch,MagicMock
from bson import ObjectId
from db import add_room_members
from pymongo.errors import DuplicateKeyError
from db import delete_user
from main import app
from unittest.mock import patch

class UserTest(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        app.config['TESTING'] = True
        self.app = app.test_client()


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
    
    def test_create_room(self):

        room_name = 'Test Room'
        members = 'user1,user2'
        data = {'room_name': room_name, 'members': members}

        response = self.app.post('/create-room/', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
    mock_rooms_collection = ...  # Define the mock_rooms_collection variable here

    # @patch('db.rooms_collection') # failing beacuse of create room
    # def test_save_room(self, mock_rooms_collection):
    #     room_name = 'Test Room'
    #     members = 'user1,user2'
    #     data = {'room_name': room_name, 'members': members}
    #     create_room(data)
    #     self.assertTrue(room_name in rooms_collection.distinct('room_name'))
        
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