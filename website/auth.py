from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_sqlalchemy import SQLAlchemy

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        check = User.query.filter(
            (User.email == email) | (User.username == username)).first()

        if check:
            flash('usename or email already in use')
        elif len(email) <= 4:
            flash('email must be longer than 4 charaters')
        elif len(username) <= 4:
            flash('usename must be longer than 4 charaters')
        elif password1 != password2:
            flash('passwords dont match')
        elif len(email) > 150 and len(username) > 150 and len(password1) > 200 and len(password2) > 200:
            flash('your inputs is too long')

        else:
            session['user'] = username
            new_user = User(username=username, email=email,
                            password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.dashboard'))

    return render_template('signup.html')


@auth.route("/signin", methods=['GET', 'POST'])
def signin():

    if 'user' in session:
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        identifier = str(request.form.get('username'))
        password = str(request.form.get('password'))

        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)).first()

        if not user:
            flash('no username')
        else:
            if check_password_hash(user.password, password) == True:
                session['user'] = user.username
                return redirect(url_for('views.dashboard'))
            else:
                flash('incorrect password')

    return render_template('signin.html')


@auth.route('/signout')
def signout():
    session.pop('user', None)
    return redirect(url_for('auth.signin'))
