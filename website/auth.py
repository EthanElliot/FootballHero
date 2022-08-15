# imports
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from itsdangerous import SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, s, mail
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user
from .forms import SignInForm, SignUpForm, SendForgotPasswordLink, ResetPassword


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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.account', username=current_user.username))

    # create form
    form = SignUpForm()

    # on form submit send email and add user to db
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = str(form.password.data)

        # send email with link
        try:
            # generate token
            token = s.dumps(email,  salt='email_verification')

            # create and send message
            msg = Message('FootballHero - Confirm your Email',
                          recipients=[email])

            link = url_for('auth.verify_email',
                           token=token, _external=True)

            msg.html = f'''<strong>Welcome to FootballHero,</strong> <br><br>
                            To verify your account click the link below:<br><br>
                            <a href={link}>verify</a> <br><br>
                            If you did not create an account, no further action is required '''

            mail.send(msg)

        except:
            abort(500)

        # add user to database
        new_user = User(username=username,
                        email=email,
                        password=generate_password_hash(password),
                        verified=False)
        db.session.add(new_user)
        db.session.commit()

        return render_template("notify.html", message_header="Before you can access your account please validate your email", message_sub="to validate your account check your email.")

    return render_template('signup.html', form=form)


# route to sign the user in
@auth.route("/signin", methods=['GET', 'POST'])
def signin():
    # check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.account', username=current_user.username))

    # create form
    form = SignInForm()

    # check info once from is validated
    if form.validate_on_submit():
        user = User.query.filter(
            (User.email == form.identifier.data) | (User.username == form.identifier.data)).first()
        # check if user is regestered
        if user:
            # check password hash
            if check_password_hash(user.password, form.password.data) == True:
                # check if user is verified
                if user.verified == True:
                    # if requiremets are met log the user in
                    login_user(user)
                    return redirect(url_for('dashboard.account', username=current_user.username))

                else:
                    flash('email is not verified')
            else:
                flash('incorrect password')
        else:
            flash('no user registered with that email or username')

    return render_template('signin.html', form=form)


# route to sign the user out
@ auth.route('/signout')
@ login_required
def signout():
    # sign the user out
    logout_user()
    return redirect(url_for('auth.signin'))


# route to verify email of the user
@ auth.route("/verify_email/<token>", methods=['GET', 'POST'])
def verify_email(token):
    try:
        email = s.loads(token, salt='email_verification', max_age=3600)
    except SignatureExpired:
        return abort(401)
    except BadSignature:
        abort(401)

    user = User.query.filter(
        (User.email == email)).first()
    user.verified = True
    db.session.commit()

    login_user(user)

    return redirect(url_for('dashboard.account', username=current_user.username))


# route for user to request update to user password
@ auth.route("/reset-password", methods=['GET', 'POST'])
def send_reset_email():
    # if user is logged in redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.account', username=current_user.username))

    form = SendForgotPasswordLink()

    # if form data is sent
    if form.validate_on_submit():
        print('yesirr')

        # get form input
        email = form.email.data
       
     

        # check the user exists
        user = User.query.filter(
            (User.email == email)).first()
        if not user:
            flash('no user registered with that email')
            return render_template('reset_password_email.html', form=form)

        # generate email
        else:
            try:
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
            except:
                abort(500)

            return render_template("notify.html", message_header="To update your password", message_sub="check your email.")
    else:
        return render_template('reset_password_email.html', form=form)


# route for user to update password
@ auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_user_password(token):
    try:
        # get token
        email = s.loads(token, salt='password_reset', max_age=3600)
    # if token expired
    except SignatureExpired:
        abort(401)
    except BadSignature:
        abort(401)

    form = ResetPassword()

    # if form input
    if form.validate_on_submit():
        # get form input
        password1 = form.password.data
        password2 = form.confirm.data

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
        return render_template('reset_password_form.html',form=form)
