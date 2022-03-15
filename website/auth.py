
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        user = session['user']
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) <= 4:
            flash('email must be longer than 4 charaters')
        elif len(username) <= 4:
            flash('usename must be longer than 4 charaters')
        elif password1 != password2:
            flash('passwords dont match')
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
    if request.method == 'POST':
        data = request.form
        print(data)
    return render_template('signin.html')
