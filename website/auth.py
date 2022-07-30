# imports
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, s, mail
from flask_mail import Mail, Message

# code for logging the sql queries (used for testing)
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# flask blueprints
auth = Blueprint('auth', __name__)


# route to sign the user up
@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    # check if user is logged in
    if 'user' in session:
        return redirect(url_for('dashboard.home'))

    # if data is sent get the form data and assign it to variables
    if request.method == 'POST':
        email = request.form.get('email')
        username = (request.form.get('username')).lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # query the database to check the username and email
        check = User.query.filter(
            (User.email == email) | (User.username == username)).first()

        print(check)
        # checks for the len of inputs and if inputs exist
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

        # if unique account sign the user up and redirect
        else:

            new_user = User(username=username, email=email,
                            password=generate_password_hash(password1), verified=False)
            db.session.add(new_user)
            db.session.commit()

            # generate token
            token = s.dumps(email,  salt='email_verification')

            # create and send message
            msg = Message('Confirm your Email', recipients=[email])

            link = url_for('auth.verify_email', token=token, _external=True)

            msg.body = 'Your link is {}'.format(link)

            mail.send(msg)

            return token

    return render_template('signup.html')


# route to sign the user in
@auth.route("/signin", methods=['GET', 'POST'])
def signin():
    # check if user is logged in
    if 'user' in session:
        return redirect(url_for('dashboard.home'))

    # if data is sent get the form data and assign it to variables
    if request.method == 'POST':
        identifier = str(request.form.get('username'))
        password = str(request.form.get('password'))

        # query the database to get the password
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier.lower())).first()

        # if no user
        if not user:
            flash('no user found')

        # if user in check the password and then if the password matches sign the user in

        else:
            print(user.verified)
            if check_password_hash(user.password, password) == True:
                if user.verified == True:
                    session['user'] = user.username
                    return redirect(url_for('dashboard.home'))

                else:
                    flash('email is not verified')

            else:
                flash('incorrect password')

    return render_template('signin.html')


# route to sign the user out
@auth.route('/signout')
def signout():
    # sign the user out
    session.pop('user', None)
    return redirect(url_for('auth.signin'))


# route to verify email of the user
@auth.route("/verify_email/<token>", methods=['GET', 'POST'])
def verify_email(token):
    try:
        email = s.loads(token, salt='email_verification', max_age=3600)
        print(email)
        user = User.query.filter(
            (User.email == email)).first()
        user.verified = True
        session["user"] = user.username
        db.session.commit()
        return(redirect(url_for('dashboard.home')))

    except SignatureExpired:
        return ('the token is expired')

    except:
        return ('something went wrong')
