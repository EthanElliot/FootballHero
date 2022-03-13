from flask import Flask, flash, redirect, render_template, request, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets


app = Flask(__name__)
# secret key
app.secret_key = secrets.token_urlsafe(32)


# using the database
DATABASE = "FootballHero.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/signin")
def signin():
    return render_template('signin.html')


@app.route("/signup_post", methods=['POST'])
def signup_post():

    username = str(request.form.get('username'))
    email = str(request.form.get('email'))

    if (str(request.form.get('password1'))) != (str(request.form.get('password2'))):
        flash('passwords dont match')
        return redirect((url_for('signup')))
    return redirect((url_for('home')))


if __name__ == "__main__":
    app.run(debug=True, port=9000, host='0.0.0.0')
