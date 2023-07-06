from flask import Blueprint, Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_migrate import Migrate
from flask_login import login_required, LoginManager, current_user
from string import ascii_uppercase
import random

from config import Config
from app.db import db
from app.models import User # noqa
from app.auth import auth


app = Flask(__name__)
app.debug = True
app.config.from_object(Config)

socketio = SocketIO(app)
app_bp = Blueprint('app_bp', __name__)

# extensions here
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# register blueprint here
app.register_blueprint(auth)


rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


@app.route("/")
def index():
    return render_template('welcome.html')


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
        return render_template('profile.html', name=current_user.name, email=current_user.email)


@app.route('/profile/edit', methods=["PUT", "POST", "GET"])
@login_required
def edit_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        update = request.form.get("update", False)

        user = User.query.get(current_user.id)

        if update != False:

            if not name and not email:
                return render_template("edit_profile.html",
                                       current_user_name=current_user.name,
                                       current_user_email=current_user.email,
                                       error="Please enter a new name or email.",
                                       email=email, name=name)

            if len(name) > 50:
                return render_template("edit_profile.html",
                                       current_user_name=current_user.name,
                                       current_user_email=current_user.email,
                                       error="! name length is no more than 50 characters !")

            if len(email) > 50:
                return render_template("edit_profile.html",
                                       current_user_name=current_user.name,
                                       current_user_email=current_user.email,
                                       error="! email length is no more than 50 characters !")

            if not name:
                user.name = current_user.name
            else:
                user.name = name

            if not email:
                user.email = current_user.email
            else:
                user.email = email

            db.session.add(user)
            db.session.commit()

            return render_template("edit_profile.html",
                            current_user_name=current_user.name,
                            current_user_email=current_user.email,
                            error="Profile update success.")

    return render_template("edit_profile.html",
                            current_user_name=current_user.name,
                            current_user_email=current_user.email)


@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    # session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        join_general_chat = request.form.get("join_general_chat", False)

        if not name:
            name = current_user.name

        if join != False and not code:
            return render_template("home.html", username=current_user.name, error="Please enter a room code.", code=code, name=name)

        room = code

        if join_general_chat != False:
            room = "AAAA"
            rooms[room] = {"members": 0, "messages": []}

        else:
            if create != False:
                room = generate_unique_code(4)
                rooms[room] = {"members": 0, "messages": []}
            elif code not in rooms:
                return render_template("home.html", username=current_user.name, error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html", username=current_user.name)


@app.route("/room")
@login_required
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")
