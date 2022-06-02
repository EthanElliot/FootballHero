# imports
import logging
from flask import Blueprint, render_template, session, redirect, url_for, abort, request, jsonify
from .models import User, Exercise, Type
from .import db
import json


# make flask blueprint
dashboard = Blueprint('dashboard', __name__)


# code for logging the sql queries (used for testing)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# function to make sqlalchemy responce jsonifyable
def to_JSON(data):
    exercises = []
    for row in data:
        exercises.append([x for x in row])
        # found from https://stackoverflow.com/questions/34715593/rows-returned-by-pyodbc-are-not-json-serializable
    return exercises


# dashboard route
@dashboard.route("/dashboard")
def home():
    # check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


# brouse route
@dashboard.route("/browse")
def browse():
    # check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('browse.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


# account route
@dashboard.route("/account")
def account():
    # check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('account.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


# create route
@dashboard.route("/create")
def create():
    # check if user is logged in
    if 'user' in session:
        user = session['user']

        types = Type.query.all()
        return render_template('create.html', username=user,  types=types)
    else:
        return redirect((url_for('auth.signin')))


# exercise route
@dashboard.route('/exercise/<int:id>')
def exercise(id):
    # check if user is logged in
    if 'user' in session:
        user = session['user']
        # query the database for exercise with the id in the route
        exercise = db.session.query(Exercise, Type).join(
            Type).filter(Exercise.id == id).first()
        # if exercise exists render the page
        if exercise:
            print(exercise)
            return render_template('exercise.html', exercise=exercise)
        # if exercise doesnt exist return a error
        else:
            abort(404)
    else:
        return redirect((url_for('auth.signin')))


@dashboard.route('/exercise-get', methods=['POST'])
def exerciseget():
    filters = json.loads(request.get_data())
    filtertext = filters['filtertext']
    filtertype = filters['filtertype']

    if filtertext and filtertype:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Exercise.name.ilike(f'%{filtertext}%'),
            Type.type == filtertype
        ).all()

        exercise_data = to_JSON(exercise_data)

    elif filtertext:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Exercise.name.ilike(f'%{filtertext}%')).all()

        exercise_data = to_JSON(exercise_data)

    elif filtertype:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Type.type == filtertype).all()

        exercise_data = to_JSON(exercise_data)

    else:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(
            Type).all()

        exercise_data = to_JSON(exercise_data)

    print(exercise_data)
    return jsonify(exercise_data)
