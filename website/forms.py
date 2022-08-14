# imports
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User


# sign in form
class SignInForm(FlaskForm):
    identifier = StringField('username or email', validators=[
                             DataRequired(), Length(min=0, max=150)], render_kw={"placeholder": "username or email"})
    password = PasswordField('password', validators=[DataRequired(), Length(min=0, max=150)], render_kw={
                             "placeholder": "password"})
    submit = SubmitField('sign in')


# sign up form
class SignUpForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(), Length(min=4, max=150)], render_kw={"placeholder": "username"})

    email = EmailField('email', validators=[
        DataRequired(), Length(min=4, max=150), Email()], render_kw={"placeholder": "email"})

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})

    confirm = PasswordField('Verify password',
                            validators=[DataRequired(), EqualTo('password',
                                                                message='Passwords must match')], render_kw={"placeholder": "Verify password"})
    submit = SubmitField('sign up')

    def validate_on_submit(self):
        email = self.email.data
        username = self.username.data
        password = self.password.data
        confirm = self.confirm.data

        # query the database to check the username and email
        check = User.query.filter(
            (User.email == email) | (User.username == username)).first()

        if check:
            flash('username or email already in use')
            return False

        if not email or not username or not password or not confirm:
            flash('plese fill out all required feilds')
            return False

        if password != confirm:
            flash('passwords dont match')
            return False

        else:
            return True
