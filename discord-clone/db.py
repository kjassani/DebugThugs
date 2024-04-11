from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient, DESCENDING
from werkzeug.security import generate_password_hash

from user import User

client = MongoClient("mongodb+srv://karimjassani24:test@discordclone.2m7im3b.mongodb.net/?retryWrites=true&w=majority&appName=discordClone")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("members")
messages_collection = chat_db.get_collection("messages")

    
def save_user(username, email, password, name, last_name):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({
        '_id': username,
        'email': email,
        'password': password_hash,
        'name': name,
        'last_name': last_name
    })
    
def update_user_profile(username, email, name, last_name):
    result = users_collection.update_one(
        {'_id': username},
        {'$set': {
            'email': email,
            'name': name,
            'last_name': last_name
        }}
    )
    return result.modified_count > 0

def delete_user(username):
    users_collection.delete_one({'_id': username})
    

def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['name'], user_data['last_name'], user_data['email'], user_data['password']) if user_data else None


def save_room(room_name, created_by, is_private=False, members=None):
    room_data = {
        'name': room_name,
        'created_by': created_by,
        'created_at': datetime.now(),
        'is_private': is_private
    }
    room_id = rooms_collection.insert_one(room_data).inserted_id
       
    
    # If it's a private chat, ensure both members are added. Otherwise, add the creator as the room member.
    if members and is_private:
        for username in members:
            add_room_member(room_id, room_name, username, created_by, is_room_admin=(username == created_by))
    else:
        add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    
    return room_id

def add_room_admin(room_id, username):
    room_members_collection.update_one({'_id': {'room_id': ObjectId(room_id), 'username': username}},
                                       {'$set': {'is_room_admin': True}})

def remove_room_admin(room_id, username):
    room_members_collection.update_one({'_id': {'room_id': ObjectId(room_id), 'username': username}},
                                       {'$set': {'is_room_admin': False}})
def get_room_admins(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id), 'is_room_admin': True}))   
def get_or_create_private_chat(user1_username, user2_username):
    # Sort usernames to ensure consistency in naming regardless of who initiates the chat
    sorted_usernames = sorted([user1_username, user2_username])
    room_name = "+".join(sorted_usernames)
    
    existing_room = rooms_collection.find_one({'name': room_name, 'is_private': True})
    if existing_room:
        return existing_room
    else:
        # Use the adjusted save_room function to create a private chat room
        room_id = save_room(room_name, sorted_usernames[0], is_private=True, members=sorted_usernames)
        return rooms_collection.find_one({'_id': room_id})



def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    room_members_collection.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})


def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})

def get_all_users():
    """
    Fetch all users from the database, excluding their password for security.
    """
    users_cursor = users_collection.find({}, {'password': 0})  # Exclude passwords from the result
    users = list(users_cursor)
    return users



def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def add_room_members(room_id, room_name, usernames, added_by):
    room_members_collection.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'added_at': datetime.now(), 'is_room_admin': False} for username in usernames])


def remove_room_members(room_id, usernames):
    room_members_collection.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(room_members_collection.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})


def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})


MESSAGE_FETCH_LIMIT = 3


def get_messages(room_id, page=0):
    offset = page * MESSAGE_FETCH_LIMIT
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]


