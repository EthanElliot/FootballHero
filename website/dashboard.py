
from flask import Blueprint, render_template, session, redirect, url_for, abort
from .models import User, Exercise, Type
from .import db


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

    exercise = db.session.query(Exercise, Type).join(Type).filter(Exercise.id == id).first()

    if exercise: 
        print(exercise)
        return render_template('exercise.html', exercise=exercise)
        

    else:
        abort(404)