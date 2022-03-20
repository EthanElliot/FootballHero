from flask import Blueprint, render_template, session, redirect, url_for


dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/dashboard")
def home():
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


@dashboard.route("/browse")
def browse():
    if 'user' in session:
        user = session['user']
        return render_template('browse.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


@dashboard.route("/account")
def account():
    if 'user' in session:
        user = session['user']
        return render_template('account.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


@dashboard.route("/create")
def create():
    if 'user' in session:
        user = session['user']
        return render_template('create.html', username=user)
    else:
        return redirect((url_for('auth.signin')))

@dashboard.route('/exercise/<int:id>')
def exercise(id):

    if 'user' in session:
        return render_template('exercise.html', id=id)
    else:
        return redirect((url_for('auth.signin')))
    