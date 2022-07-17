# imports
import logging
import queue
from flask import Blueprint, render_template, session, redirect, url_for, abort, request, jsonify
from .models import User, Exercise, Type, Program, ExerciseProgram, FavoriteProgram
from .import db
import json
from werkzeug.security import check_password_hash
from sqlalchemy import asc, func, column, desc, false


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
        # get user info from the db
        user = db.session.query(User).filter(
            User.username == session['user']).first()

        # if user dosent exist return 404 error
        if not user:
            abort(404)

        # get the of plalists created by the user
        programscreated = db.session.query(Program.id, Program.name).filter(
            (Program.user_id == int(user.id))).all()

        # get the programs that the user has favorited
        UserFavorites = user.favorites.all()

        # get the programs with the most favorites
        mostfavorites = db.session.query(
            FavoriteProgram.columns.program_id.label('id'), Program.name).join(Program).group_by(FavoriteProgram.columns.program_id).order_by(desc(func.count(FavoriteProgram.columns.program_id))).limit(5).all()

        # render the page
        return render_template('dashboard.html', user=user, programscreated=programscreated, UserFavorites=UserFavorites, mostfavorites=mostfavorites)
    else:
        return redirect((url_for('auth.signin')))


# brouse route
@dashboard.route("/browse")
def browse():
    # check if user is logged in a
    if 'user' in session:
        # if the user searches something
        if request.args and len(request.args.get('query')) > 0:
            query = request.args.get('query')
            orderby = request.args.get('orderby')

            return render_template('browse.html', query=query, orderby=orderby)

        else:
            return render_template('browse.html')
    else:
        return redirect((url_for('auth.signin')))


# account route
@dashboard.route("/account/<username>")
def account(username):
    # check if user is logged in
    if 'user' in session:

        # get user info from the db
        user = db.session.query(User).filter(
            User.username == username).first()

        # if user dosent exist return 404 error
        if not user:
            abort(404)

        # get the programs with the favorites count added
        likes_query = db.session.\
            query(
                FavoriteProgram.columns.program_id.label('programid'),
                func.count().label('cnt')
            ).\
            filter(FavoriteProgram.columns.program_id).\
            group_by('programid').\
            subquery()

        programscreated = db.session.\
            query(Program.id,
                  Program.name,
                  func.coalesce(
                      likes_query.c.cnt, 0).label('cnt')
                  ).\
            join(likes_query,
                 likes_query.c.programid == Program.id,
                 isouter=True
                 ).\
            filter(Program.user_id == user.id).\
            order_by(desc(Program.id)).\
            all()

        # render the page
        return render_template('account.html', user=user, programscreated=programscreated)
    else:
        return redirect((url_for('auth.signin')))


# create route
@dashboard.route("/create")
def create():
    # check if user is logged in
    if 'user' in session:
        # get the exercise types
        types = Type.query.all()

        return render_template('create.html',  types=types)
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
    # get the filters for the exercises
    filters = json.loads(request.get_data())
    filtertext = filters['filtertext']
    filtertype = filters['filtertype']

    # if filtering by both filters
    if filtertext and filtertype:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Exercise.name.ilike(f'%{filtertext}%'),
            Type.type == filtertype
        ).all()

        exercise_data = to_JSON(exercise_data)

    # if filtering by text filter
    elif filtertext:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Exercise.name.ilike(f'%{filtertext}%')).all()

        exercise_data = to_JSON(exercise_data)

    # if filtering by type filter
    elif filtertype:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(Type).filter(
            Type.type == filtertype).all()

        exercise_data = to_JSON(exercise_data)

    # if no filter
    else:
        exercise_data = db.session.query(Exercise.id, Exercise.name, Type.type).join(
            Type).all()

        exercise_data = to_JSON(exercise_data)

    # return the exercises
    return jsonify(exercise_data)

# create program route


@dashboard.route('/create-program', methods=['POST'])
def create_program():
    # check user is logged in
    if 'user' in session:
        # load the exercise data and assign them to variables
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

        # return the exercise program
        return jsonify(True, programid)

    else:
        return jsonify(False, ' user not logged in')


# route for delete program
@dashboard.route('/delete-program', methods=['POST'])
def delete_program():
    # check that user is logged in
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


# route for like program
@dashboard.route('/like-program', methods=['POST'])
def like_program():
    # check if user is logged in
    if 'user' in session:
        # get the program id that we will delete
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


# program route
@dashboard.route('/program/<int:id>')
def program(id):
    # check if user is logged in
    if 'user' in session:
        # set the user to the logged in user
        user = session['user']

        # get the program info
        program_info = db.session.query(
            Program.id, Program.name, Program.description, User.username).join(User).filter(Program.id == id).first()

        # if program dosent exist return 404
        if not program_info:
            abort(404)

        # get the exercises from the program
        exercises = Program.query.filter(Program.id == id).first().exercises

        # this is used to check if user has liked the program... returns true if they have and returns false if they havent
        # get the id of the user
        user_id = db.session.query(User.id).filter(
            User.username == user).first()

        # query the favoriteProgram relationship to see if the user id has liked the program with the id of the entered id.
        user_like = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.user_id == int(user_id[0])) & (FavoriteProgram.columns.program_id == int(id))).first()

        if user_like:
            liked_by_user = True
        else:
            liked_by_user = False

        # get amount of likes
        likes = db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.program_id == int(id))).count()

        # render page
        return render_template('program.html', username=user, program_info=program_info, exercises=exercises, liked_by_user=liked_by_user, likes=likes)
    else:
        return redirect((url_for('auth.signin')))


# route for delete account
@ dashboard.route('/delete-account', methods=['POST'])
def delete_account():
    # check if user is logged in
    if 'user' in session:
        # get the user data
        userdata = json.loads(request.get_data())

        # check that the user that is logged in is the one that sends the request.

        if session['user'] == userdata['username']:
            # get the user info
            user = db.session.query(User).filter(
                User.username == session['user']).first()
            if check_password_hash(user.password, userdata['password']) == True:

                # delete program
                program_id = db.session.query(Program.id).filter(
                    Program.user_id == user.id).first()

                # if user has created programs delete
                if program_id:
                    db.session.query(ExerciseProgram).filter(
                        ExerciseProgram.columns.program_id == program_id[0]).delete()
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

                # log user out
                session.pop('user', None)
                return jsonify(True, 'Success')

            else:
                return jsonify(False, 'Incorect password')

        else:
            return jsonify(False, 'Something went wrong')

    else:
        return jsonify(False, 'User not logged in')


# route for editing account info
@ dashboard.route('/edit-account', methods=['POST'])
def edit_account():
    # check if user is logged in
    if 'user' in session:
        userdata = json.loads(request.get_data())

        # check that the user that is logged in is the one that sends the request.
        if session['user'] == userdata['username']:
            # get the users accout info
            user = db.session.query(User).filter(
                User.username == session['user']).first()

            # if user doesnt exist
            if not user:
                return jsonify(False, 'Something went wrong')

            # check password hash
            if check_password_hash(user.password, userdata['password']) == True:

                # assign the new userdata to variables
                new_username = str(userdata['updateinfo']['username']).lower()
                new_email = str(userdata['updateinfo']['email'])

                # create a check for the email and username
                # if user has changed both email and username
                if user.username != new_username and user.email != new_email:
                    check = User.query.filter(
                        (User.email == new_email) | (User.username == new_username)).first()
                # if user has changed just username
                elif user.username != new_username:
                    check = User.query.filter(
                        (User.username == new_username)).first()

                # if user has changed email
                elif user.email != new_email:
                    check = User.query.filter(
                        (User.email == new_email)).first()
                # if user didnt change anything
                else:
                    return jsonify(True, session['user'])

                # checks before updating the data
                if check:
                    return jsonify(False, 'email or username already in use')
                if len(new_email) <= 4:
                    return jsonify(False, 'email must be longer than 4 charaters')
                if len(new_username) <= 4:
                    return jsonify(False, 'usename must be longer than 4 charaters')
                if len(new_email) > 150 and len(new_username) > 150:
                    return jsonify(False, 'your inputs are too long')
                else:
                    # update the user info
                    user.username = (new_username)
                    user.email = (new_email)
                    db.session.commit()
                    session['user'] = new_username
                    return jsonify(True, new_username)

            else:

                return jsonify(False, 'Incorect password')

        else:
            return jsonify(False, 'Something went wrong')

    else:
        return jsonify(False, 'User not logged in')


# route for load program
@dashboard.route('/load-programs', methods=['POST'])
def load_programs():
    # assign the query to variables
    request_data = json.loads(request.get_data())
    # startpoint of count
    count = request_data['c']
    query = str(request_data['query'])
    orderby = str(request_data['orderby'])

    # query the database
    likes_query = db.session.\
        query(
            FavoriteProgram.columns.program_id.label('programid'),
            func.count().label('cnt')
        ).\
        filter(FavoriteProgram.columns.program_id).\
        group_by('programid').\
        subquery()

    programscreated = db.session.\
        query(Program.id,
              Program.name,
              func.coalesce(
                  likes_query.c.cnt, 0).label('cnt'),
              User.username
              ).\
        join(likes_query,
             likes_query.c.programid == Program.id,
             isouter=True
             ).join(User).\
        filter(Program.name.like(f'%{query}%'))

    # create outcome based on orderby (order of the posts)
    if not orderby:
        return jsonify(to_JSON(programscreated.limit(6).offset(count).all()))

    elif orderby == 'newest':
        programscreated = programscreated.order_by(
            desc(Program.id)).limit(6).offset(count).all()
        return jsonify(to_JSON(programscreated))

    elif orderby == 'oldest':
        programscreated = programscreated.order_by(
            asc(Program.id)).limit(6).offset(count).all()
        return jsonify(to_JSON(programscreated))

    elif orderby == 'most_liked':
        programscreated = programscreated.order_by(
            desc(likes_query.c.cnt)).limit(6).offset(count).all()
        return jsonify(to_JSON(programscreated))

    elif orderby == 'least_liked':
        programscreated = programscreated.order_by(
            asc(likes_query.c.cnt)).limit(6).offset(count).all()
        return jsonify(to_JSON(programscreated))
    else:
        return jsonify(to_JSON(programscreated.limit(6).offset(count).all()))
