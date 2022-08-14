# imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


# sign in form
class SignInForm(FlaskForm):
    identifier = StringField('username or email', validators=[
                             DataRequired(), Length(min=0, max=200)], render_kw={"placeholder": "username or email"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={
                             "placeholder": "password"})
    submit = SubmitField('sign in')
