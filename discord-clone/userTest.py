import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from db import save_user, get_user, users_collection
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

    def test_save_user(self):
        user = User(username='testuser', password='password123')
        save_user(user)
        saved_user = get_user('testuser')
        self.assertEqual(saved_user.username, 'testuser')

    def test_duplicate_user(self):
        user = User(username='testuser', password='password123')
        with self.assertRaises(DuplicateKeyError):
            save_user(user)