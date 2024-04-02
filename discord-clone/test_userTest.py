import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from db import save_user, get_user, users_collection, delete_user
from pymongo.errors import DuplicateKeyError
from main import app
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user, LoginManager

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
        response = self.app.post('/login', data=dict(username='zain', password='password123'), follow_redirects=True)
    
    def test_save_message(self):
        room_id = 1
        text = 'hello'
        sender = get_user('zain')
        time = datetime.now()
        save_message(room_id,text,sender) 
        self.assertTrue({room_id, text, sender} in db.messages_collection)
        
        

if __name__ == '__main__':
    unittest.main()