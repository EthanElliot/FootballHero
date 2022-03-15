from flask import Blueprint, render_template, session, redirect, url_for


views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template('home.html')


@views.route("/dashboard")
def dashboard():
    if 'user' in session:
        user = session['user']
        print(user)
        return render_template('dashboard.html', username=user)
    else:
        return redirect((url_for('auth.signin')))
