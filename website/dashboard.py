# imports
import logging
from flask import Blueprint, render_template, session, redirect, url_for, abort, request, jsonify
from .models import User, Exercise, Type, Program, ExerciseProgram, FavoriteProgram
from .import db
import json
from werkzeug.security import check_password_hash


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
@dashboard.route("/account/<username>")
def account(username):
    # check if user is logged in
    if 'user' in session:
        user = db.session.query(User.id, User.username).filter(
            User.username == username).first()

        if not user:
            abort(404)

        playlistcreated = db.session.query(Program.user_id).filter(
            (Program.user_id == int(user.id))).count()
        return render_template('account.html', user=user, playlistcreated=playlistcreated)
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

    return jsonify(exercise_data)


@dashboard.route('/create-program', methods=['POST'])
def create_program():
    if 'user' in session:
        if request.method == 'POST':
            exercisedata = json.loads(request.get_data())
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
                return jsonify(False, 'Not enough exercises selected.')
            if len(name) > 16:
                return jsonify(False, 'Name is too long.')
            if len(description) > 60:
                return jsonify(False, 'Description is too long.')
            if len(exercises) > 40:
                return jsonify(False, 'Too many exercises selected.')

            # check for duplicates

            exerciseids = []
            for exercise in exercises:
                exerciseids.append(exercise[0])

            if len(exerciseids) != len(set(exerciseids)):
                return jsonify(False, 'There are duplicate exercises')

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


@dashboard.route('/delete-program', methods=['POST'])
def delete_program():
    if 'user' in session:
        programdata = json.loads(request.get_data())

        # check if the user deleting the program is the user logged in in session data
        if session['user'] != programdata['username']:
            return jsonify(False)

        # delete data from all tables where id is the id sent.
        # *not sure if this is the propprer way to do this some guidance would be appreciated*
        db.session.query(ExerciseProgram).filter(
            ExerciseProgram.columns.program_id == programdata['id']).delete()
        db.session.query(FavoriteProgram).filter(
            FavoriteProgram.columns.program_id == programdata['id']).delete()
        Program.query.filter(Program.id == programdata['id']).delete()
        db.session.commit()

        return jsonify(True)
    else:
        return jsonify(False)


@dashboard.route('/like-program', methods=['POST'])
def like_program():
    if 'user' in session:
        programdata = json.loads(request.get_data())
        program_id = programdata['id']

        # this is used to check if user has liked the program... returns true if they have and returns false if they havent
        # get the id of the user
        user_id = db.session.query(User.id).filter(
            User.username == session['user']).first()

        # query the favoriteProgram relationship to see if the user id has liked the program with the id of the entered id.
        user_like = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.user_id == int(user_id[0])) & (FavoriteProgram.columns.program_id == program_id)).first()

        # create outcome and add the relationship if the user hasnt liked or remove if they have
        if user_like:
            db.session.query(FavoriteProgram).filter(
                (FavoriteProgram.columns.user_id == int(user_id[0])) & (FavoriteProgram.columns.program_id == program_id)).delete()
            db.session.commit()
            liked_by_user = False

        else:
            likerelationship = FavoriteProgram.insert().values(
                user_id=(user_id.id), program_id=(program_id))
            db.session.execute(likerelationship)
            db.session.commit()
            liked_by_user = True

        # get like count
        likes = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.program_id == int(program_id))).count()

        # create responce
        response = {
            'liked_by_user': liked_by_user,
            'likes': likes
        }

        # return responce
        return jsonify(response)
    else:
        return jsonify('error: user not logged in')


@dashboard.route('/program/<int:id>')
def program(id):
    if 'user' in session:
        user = session['user']

        program_info = db.session.query(
            Program.id, Program.name, Program.description, User.username).join(User).filter(Program.id == id).first()

        if not program_info:
            abort(404)

        exercises = Program.query.filter(Program.id == id).first().exercises

        # this is used to check if user has liked the program... returns true if they have and returns false if they havent
        # get the id of the user
        user_id = db.session.query(User.id).filter(
            User.username == user).first()

        # query the favoriteProgram relationship to see if the user id has liked the program with the id of the entered id.
        user_like = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.user_id == int(user_id[0])) & (FavoriteProgram.columns.program_id == int(id))).first()

        # create outcome
        if user_like:
            liked_by_user = True
        else:
            liked_by_user = False

        # get amount of likes
        likes = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.program_id == int(id))).count()

        return render_template('program.html', username=user, program_info=program_info, exercises=exercises, liked_by_user=liked_by_user, likes=likes)
    else:
        return redirect((url_for('auth.signin')))


@dashboard.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user' in session:
        userdata = json.loads(request.get_data())

        if session['user'] == userdata['username']:
            user = db.session.query(User).filter(
                User.username == session['user']).first()
            if check_password_hash(user.password, userdata['password']) == True:

                # delete program
                program_id = db.session.query(Program.id).filter(
                    Program.user_id == user.id).first()

                if program_id:
                    db.session.query(ExerciseProgram).filter(
                        ExerciseProgram.columns.program_id == program_id).delete()
                    db.session.query(Program).filter(
                        Program.user_id == user.id).delete()
                    db.session.query(FavoriteProgram).filter(
                        FavoriteProgram.columns.program_id == program_id[0]).delete()

                # delete favorited programs
                db.session.query(FavoriteProgram).filter(
                    FavoriteProgram.columns.user_id == user.id).delete()

                # delete user
                db.session.query(User).filter(User.id == user.id).delete()

                # commit
                db.session.commit()

                session.pop('user', None)
                return jsonify(True, 'Success')

            else:
                return jsonify(False, 'Incorect password')

        else:
            return jsonify(False, 'Something went wrong')

    else:
        return jsonify(False, 'User not logged in')
