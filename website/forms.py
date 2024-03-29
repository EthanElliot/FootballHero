# imports
from flask import flash
from flask_wtf import FlaskForm
from sqlalchemy import false
from wtforms import StringField, PasswordField, SubmitField,\
    EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User


# sign in form
class SignInForm(FlaskForm):
    identifier = StringField('username or email',
                             validators=[
                                 DataRequired(),
                                 Length(min=0, max=150)],
                             render_kw={
                                 "placeholder": "username or email"
                             }
                             )
    password = PasswordField('password',
                             validators=[
                                 DataRequired(),
                                 Length(min=0, max=150)],
                             render_kw={
                                 "placeholder": "password"
                             }
                             )
    submit = SubmitField('sign in')


# sign up form
class SignUpForm(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=4, max=150)
        ],
        render_kw={"placeholder": "username"})

    email = EmailField(
        'email',
        validators=[
            DataRequired(),
            Length(min=4, max=150),
            Email()
        ],
        render_kw={"placeholder": "email"})

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4, max=150)
        ],
        render_kw={"placeholder": "Password"})

    confirm = PasswordField(
        'Verify password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Verify password"})
    submit = SubmitField('sign up')

    def validate_on_submit(self):
        email = str(self.email.data)
        username = str(self.username.data)
        password = self.password.data
        confirm = self.confirm.data

        # make username lower case for checks
        username = username.lower()

        # query the database to check the username and email
        check = User.query.filter(
            (User.email == email) | (User.username == username)).first()

        if check:
            flash('username or email already in use')
            return False

        if not email or not username or not password or not confirm:
            return False
        if len(email) <= 4:
            flash('email must be longer than 4 charaters')
            return False
        if len(username) <= 4:
            flash('usename must be longer than 4 charaters')
            return False
        if len(password) < 1:
            flash('password to short')
            return False
        if len(email) > 150 and len(username) > 150 \
                and len(password) > 150 and len(confirm) > 150:
            flash('your inputs are to long')
            return False

        if password != confirm:
            flash('passwords dont match')
            return False

        for char in username:
            if char not in [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', '0', "1", '2', '3',
                    '4', '5', '6', '7', '8', '9']:
                flash(f'{char} not allowed')
                return False

        else:
            return True


class SendForgotPasswordLink(FlaskForm):
    email = EmailField(
        'email',
        validators=[
            DataRequired(),
            Length(min=4, max=150),
            Email()
        ],
        render_kw={"placeholder": "email"})
    submit = SubmitField('reset')


class ResetPassword(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4, max=150)
        ],
        render_kw={"placeholder": "Password"})

    confirm = PasswordField(
        'Verify password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Verify password"})
    submit = SubmitField('reset')


class BrowsePrograms(FlaskForm):
    query = StringField(
        'keywords',
        validators=[
            Length(min=0, max=150)
        ],
        render_kw={"placeholder": "keywords"})
    filter = SelectField(
        'filter',
        choices=[
            ("", "Filter"),
            ("newest", "Newest"),
            ("oldest", "Oldest"),
            ("most_liked", "Most liked"),
            ("least_liked", "Least liked")
        ],
        default=("", "Filter"))
    submit = SubmitField('search')


class AccountEditInfo(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=4, max=150)
        ],
        render_kw={"placeholder": "username"})

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(max=150)
        ],
        render_kw={"placeholder": "Password"})
    edit = SubmitField('Edit')

    def validate_on_submit(self):
        username = str(self.username.data)

        # make username lower case for checks
        username = username.lower()

        # query the database to check the username and email
        check = User.query.filter(User.username == username).first()

        if check:
            return False

        if not username:
            return False

        if len(username) <= 4:

            return False

        if len(username) > 150:
            return False

        for char in username:
            if char not in [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', '0', "1", '2', '3',
                    '4', '5', '6', '7', '8', '9']:

                return False

        else:
            return True


class AccountDelete(FlaskForm):

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(max=150)
        ],
        render_kw={"placeholder": "Password"})

    delete = SubmitField('Delete')
