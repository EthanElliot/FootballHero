from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from .models import User
from flask import flash
from flask_login import login_user


class SignInForm(FlaskForm):
    identifier = StringField('username or email', validators=[
                             DataRequired(), Length(min=0, max=200)], render_kw={"placeholder": "username or email"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={
                             "placeholder": "password"})
    submit = SubmitField('sign in')
