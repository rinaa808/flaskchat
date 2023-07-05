from flask import Blueprint, render_template, redirect, url_for, request
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return render_template('login_error.html')

    login_user(user, remember=remember)
    return redirect(url_for('home'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return render_template('signup_error.html')

    if not email or not name or not password:
        return render_template("signup.html", error="please enter a details")

    if len(email) > 50:
        return render_template("signup.html", error="! email length is no more than 50 characters !")

    if len(password) > 20:
        return render_template("signup.html", error="! password length is no more than 20 characters !")

    if len(name) > 50:
        return render_template("signup.html", error="! name length is no more than 50 characters !")

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
