from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash  

from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError
from bson.json_util import dumps

from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError


from db import get_user, save_user, get_rooms_for_user, get_room, is_room_member, get_room_members, add_room_member, add_room_members, \
    remove_room_members, update_room, is_room_admin, save_room, get_messages,save_message, get_all_users, \
    get_or_create_private_chat, update_user_profile, add_room_admin, remove_room_admin, get_room_admins, delete_message, get_one_message

app = Flask(__name__)
app.secret_key = "sfdjkafnk"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    message = request.args.get('message', '')
    rooms = []
    users = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
        users = get_all_users()  # Use the get_all_users method to fetch the list of users
    return render_template("index.html", rooms=rooms, users=users, message = message)

@app.route('/start_private_chat/<username>', methods=['GET'])
@login_required
def start_private_chat(username):
    if current_user.username == username:
        return jsonify({'error': 'Cannot start a chat with yourself.'}), 400

    room = get_or_create_private_chat(current_user.username, username)
    if room:
        # Return the room_id in JSON format
        return jsonify({'room_id': str(room['_id'])})
    else:
        return jsonify({'error': 'Unable to create or find a chat room.'}), 500

@app.route('/edit_profile')
@login_required
def edit_profile():
    # Fetch current user details to pre-populate the form
    user = get_user(current_user.username)
    # username = user.username
    # first_name = user.first_name
    # last_name = user.last_name
    if user:
        return render_template('edit_profile.html', user=user)
    else:
        return "User not found", 404



    
@app.route('/submit_edit_profile', methods=['POST'])
@login_required
def submit_edit_profile():
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    
    updated = update_user_profile(current_user.username, email, name, last_name)
    if updated:
        return redirect(url_for('home', message='Profile successfully updated'))
    else:
        return 'Error updating profile', 400



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        try:
            save_user(username, email, password, name, last_name)
            main_server_room_id = '6618489b14d6b21ccee19216'
            main_server_room = get_room(main_server_room_id)
            add_room_member(main_server_room_id, 'Main Server', username, 'admin2')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for('view_room', room_id=room_id))
        else:
            message = "Failed to create room"
    return render_template('create_room.html', message=message)



@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        existing_room_admins = [admin['_id']['username'] for admin in get_room_admins(room_id)]
        room_members_str = ",".join(existing_room_members)
        room_admins_str = ",".join(existing_room_admins)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            new_admins = [username.strip() for username in request.form.get('admins').split(',')]
            admins_to_add = list(set(new_admins) - set(existing_room_admins))
            admins_to_remove = list(set(existing_room_admins) - set(new_admins))
            if len(admins_to_add):
                for admin in admins_to_add:
                    add_room_admin(room_id, admin)
            if len(admins_to_remove):
                for admin in admins_to_remove:
                    remove_room_admin(room_id, admin)
            message = 'Room edited successfully'
            room_members_str = ",".join(new_members)
            room_admins_str = ",".join(new_admins)
        return render_template('edit_room.html', room=room, room_members_str=room_members_str,room_admins_str=room_admins_str, message=message)
    else:
        return "Acces not allowed: not an admin", 404


@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        is_admin = is_room_admin(room_id, current_user.username)
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages,is_room_admin=is_admin)
    else:
        return "Room not found", 404

@app.route('/delete_message', methods=['POST'])
@login_required
def handle_delete_message():
    message_id = request.form.get('message_id')
    message = get_one_message(message_id)
    room_id = message['room_id']
    if is_room_admin(room_id, current_user.username):
        delete_message(message_id)
    return redirect(url_for('view_room', message='Message successfully deleted'))

@app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])
    



@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])



@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)