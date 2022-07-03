# imports
import logging
from operator import le
from flask import Blueprint, render_template, session, redirect, url_for, abort, request, jsonify
from .models import User, Exercise, Type, Program, ExerciseProgram
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


@dashboard.route('/create-program', methods=['POST'])
def create_program():
    if 'user' in session:
        if request.method == 'POST':
            exercisedata = json.loads(request.get_data())
            print(exercisedata)
            name = exercisedata['name']
            description = exercisedata['description']
            username = session['user']
            exercises = exercisedata['exercises']

            # checks for form inupt
            if not name:
                return jsonify(False, 'No name given.')
            if not description:
                return jsonify(False, 'No description given.')
            if not exercises:
                return jsonify(False, 'No exercises selected.')
            if len(name) < 4:
                return jsonify(False, 'Name is too short.')
            if len(description) < 20:
                return jsonify(False, 'Description is too short.')
            if len(exercises) < 2:
                return jsonify(False, 'Not enouph exercises selected.')
            if len(name) > 16:
                return jsonify(False, 'Name is too long.')
            if len(description) > 60:
                return jsonify(False, 'Description is too long.')
            if len(exercises) > 40:
                return jsonify(False, 'Too many exercises selected.')

            # get user id
            userid = User.query.filter_by(username=f'{username}').first().id
            # insert playlist data into table.
            program = Program(
                name=name, description=description, user_id=userid)
            db.session.add(program)
            db.session.commit()

            # get id of added program
            programid = program.id

            # insert the exercises into the ExerciseProgram table

            for i in range(len(exercises)):
                exerciseprogram = ExerciseProgram.insert().values(
                    program_id=programid, exercise_id=exercises[i][0])
                db.session.execute(exerciseprogram)
                db.session.commit()

            return jsonify(True, programid)
