# imports
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, abort
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, s, mail
from flask_mail import Message

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
        elif len(password1) < 1:
            flash('password to short')
        elif password1 != password2:
            flash('passwords dont match')
        elif len(email) > 150 and len(username) > 150 and len(password1) > 200 and len(password2) > 200:
            flash('your inputs are to long')

        # if unique account sign the user up and redirect
        else:

            new_user = User(username=username, email=email,
                            password=generate_password_hash(password1), verified=False)
            db.session.add(new_user)
            db.session.commit()

            # generate token
            token = s.dumps(email,  salt='email_verification')

            # create and send message
            msg = Message('FootballHero - Confirm your Email',
                          recipients=[email])

            link = url_for('auth.verify_email', token=token, _external=True)

            msg.html = f'''<strong>Welcome to FootballHero,</strong> <br><br> 
                            To verify your account click the link below:<br><br> 
                            <a href={link}>verify</a> <br><br> 
                            If you did not create an account, no further action is required '''

            mail.send(msg)

            return render_template("notify.html", message_header="Before you can access your account please validate your email", message_sub="to validate your account check your email.")

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
        return abort(401)

    except:
        return ('something went wrong')


# route for user to request update to user password
@auth.route("/reset-password", methods=['GET', 'POST'])
def send_reset_email():
    # if user is logged in redirect to dashboard
    if 'user' in session:
        return redirect(url_for('dashboard.home'))

    # if form data is sent
    if request.method == 'POST' and request.form:
        # get form input
        email = str(request.form.get('email'))

        # check the user exists
        user = User.query.filter(
            (User.email == email)).first()
        if not user:
            flash('no user registered with that email')
            return render_template('reset_password_email.html')

        # generate email
        else:
            token = s.dumps(email,  salt='password_reset')

            # create and send message
            msg = Message('FootballHero - Reset Your password',
                          recipients=[email])

            link = url_for('auth.reset_user_password',
                           token=token, _external=True)

            msg.html = f'''<strong>Reset password,</strong> <br><br> 
                            To reset your password click the link below:<br><br> 
                            <a href={link}>reset</a> <br><br> 
                            If you did try to reset your password, no further action is required '''

            mail.send(msg)
            return render_template("notify.html", message_header="To update your password", message_sub="check your email.")

    else:
        return render_template('reset_password_email.html')


# route for user to update password
@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_user_password(token):
    try:
        # get token
        email = s.loads(token, salt='password_reset', max_age=3600)
        # if form input
        if request.method == 'POST' and request.form:
            # get form input
            password1 = str(request.form.get('password1'))
            password2 = str(request.form.get('password2'))

            # check passwords
            if password1 != password2:
                flash('passwords dont match')
                return render_template('reset_password_form.html')
            elif len(password1) > 200 and len(password2) > 200:
                flash('your inputs are too long')
                return render_template('reset_password_form.html')
            elif len(password1) < 1:
                flash('password to short')
                return render_template('reset_password_form.html')

            # if passwords are valid update the db
            User.query.filter_by(email=email).update(
                dict(password=generate_password_hash(password1)))
            db.session.commit()
            # redirect to login
            flash('password updated')
            return redirect(url_for('auth.signin'))
        else:
            return render_template('reset_password_form.html')

    # if token expired
    except SignatureExpired:
        abort(401)

    # if any other error
    except:
        abort(500)
