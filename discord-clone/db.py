from pymongo import MongoClient, DESCENDING
from werkzeug.security import generate_password_hash
from user import User
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb+srv://karimjassani24:test@discordclone.2m7im3b.mongodb.net/?retryWrites=true&w=majority&appName=discordClone")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
members_collection = chat_db.get_collection("members")
messages_collection = chat_db.get_collection("messages")


def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})

def delete_user(username):
    users_collection.delete_one({'_id': username})
# save_user("john", "hasan@gmail.com", "test123")

def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None

def save_room(room_name, created_by):
    room_id = rooms_collection.insert_one(
        {'name': room_name, 'created_by': created_by}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    return room_id

def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'is_room_admin': is_room_admin})

def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    members_collection.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})
    
def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})

def add_room_members(room_id, room_name, usernames, added_by):
    members_collection.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
           'is_room_admin': False} for username in usernames])
    
def remove_room_members(room_id, usernames):
    members_collection.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})
    
def get_room_members(room_id):
    return list(members_collection.find({'_id.room_id': ObjectId(room_id)}))

def is_room_member(room_id, username):
    return members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})

def is_room_admin(room_id, username):
    return members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})
    
def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'message_time': datetime.now()})

message_limit = 3

def get_messages(room_id, page=0):
    offset_value = page * message_limit
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(message_limit).skip(offset_value))
    for message in messages:
        message['message_time'] = message['message_time'].strftime("%d %b, %H:%M")
    return messages[::-1] #the -1 makes the messages be displayed in the right order
