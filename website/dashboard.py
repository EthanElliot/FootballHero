# imports
import logging
from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify, make_response
from .models import User, Exercise, Type, Program, ExerciseProgram, FavoriteProgram
from .import db
import json
from werkzeug.security import check_password_hash
from sqlalchemy import asc, func, column, desc, false
from flask_login import login_required, current_user
from .forms import BrowsePrograms, AccountEditInfo, AccountDelete


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


# brouse route
@dashboard.route("/browse", methods=['GET', "POST"])
@login_required
def browse():
    form = BrowsePrograms()
    # if the user searches something
    if form.validate_on_submit():
        query = form.query.data
        orderby = form.filter.data

        form.filter.default = orderby
        form.query.default = query

        return render_template('browse.html', form=form, query=query, orderby=orderby)

    else:
        return render_template('browse.html', form=form)


# account route
@dashboard.route("/account/<username>", methods=['POST', 'GET'])
@login_required
def account(username):

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

    if username == current_user.username:
        Editform = AccountEditInfo()
        DeleteForm = AccountDelete()

        # edit account
        if Editform.validate_on_submit() and Editform.edit.data:
            user = db.session.query(User).filter(
                User.username == current_user.username).first()
            if check_password_hash(user.password, DeleteForm.password.data) == True:
                new_username = Editform.username.data

                check = User.query.filter(
                    (User.username == new_username)).first()
                # checks before updating the data
                if not check:
                    # update the user info
                    print(new_username)
                    user.username = (new_username)
                    db.session.commit()
                    current_user.username = new_username
                    return redirect(url_for('dashboard.account', username=new_username))

        # delete account
        if DeleteForm.validate_on_submit() and DeleteForm.delete.data:
            user = db.session.query(User).filter(
                User.username == current_user.username).first()
            if check_password_hash(user.password, DeleteForm.password.data) == True:
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

                return redirect(url_for('views.home'))

        Editform.username.data = current_user.username
        # render the page
        return render_template('account.html', user=user, programscreated=programscreated, Editform=Editform, DeleteForm=DeleteForm)

    # render the page
    return render_template('account.html', user=user, programscreated=programscreated)


# create route
@dashboard.route("/create")
@login_required
def create():
    # get the exercise types
    types = Type.query.all()

    return render_template('create.html',  types=types)


# exercise route
@dashboard.route('/exercise/<int:id>')
@login_required
def exercise(id):
    # query the database for exercise with the id in the route
    exercise = db.session.\
        query(
            Exercise,
            Type).\
        join(Type).\
        filter(
            Exercise.id == id
        ).\
        first()
    # if exercise exists render the page
    if exercise:
        return render_template('exercise.html', exercise=exercise)
    # if exercise doesnt exist return a error
    else:
        abort(404)


@dashboard.route('/exercise-get', methods=['POST'])
def exerciseget():
    # get the filters for the exercises
    filters = json.loads(request.get_data())
    filtertext = filters['filtertext']
    filtertype = filters['filtertype']

    exercise_data = db.session.\
        query(
            Exercise.id,
            Exercise.name,
            Type.type).\
        join(Type)

    # if filtering by both filters
    if filtertext and filtertype:
        exercise_data = exercise_data.\
            filter(
                Exercise.name.ilike(f'%{filtertext}%'),
                Type.type == filtertype
            ).\
            all()

        exercise_data = to_JSON(exercise_data)

    # if filtering by text filter
    elif filtertext:
        exercise_data = exercise_data.\
            filter(
                Exercise.name.ilike(f'%{filtertext}%')
            ).\
            all()

        exercise_data = to_JSON(exercise_data)

    # if filtering by type filter
    elif filtertype:
        exercise_data = exercise_data.\
            filter(
                Type.type == filtertype).\
            all()

        exercise_data = to_JSON(exercise_data)

    # if no filter
    else:
        exercise_data = exercise_data.all()

        exercise_data = to_JSON(exercise_data)

    # return the exercises
    response = make_response(jsonify(exercise_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


# create program route
@dashboard.route('/create-program', methods=['POST'])
@login_required
def create_program():
    # load the exercise data and assign them to variables
    exercisedata = json.loads(request.get_data())
    name = exercisedata['name']
    description = exercisedata['description']
    userid = current_user.id
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
        return jsonify(False, 'Not enough exercises selected.(min:2)')
    if len(name) > 16:
        return jsonify(False, 'Name is too long.')
    if len(description) > 60:
        return jsonify(False, 'Description is too long.')
    if len(exercises) > 40:
        return jsonify(False, 'Too many exercises selected.(max:40)')

    # check for duplicates
    exerciseids = []
    for exercise in exercises:
        exerciseids.append(exercise[0])

    if len(exerciseids) != len(set(exerciseids)):
        return jsonify(False, 'There are duplicate exercises')

    # insert playlist data into table.
    program = Program(
        name=name, description=description, user_id=userid)
    db.session.add(program)
    db.session.commit()

    # insert the exercises into the ExerciseProgram table
    for i in range(len(exercises)):
        exerciseprogram = ExerciseProgram.insert().values(
            program_id=program.id, exercise_id=exercises[i][0])
        db.session.execute(exerciseprogram)

    db.session.commit()

    # return the exercise program
    return jsonify(True, program.id)


# route for delete program
@dashboard.route('/delete-program', methods=['POST'])
def delete_program():
    # check that user is logged in
    programdata = json.loads(request.get_data())

    # check if the user deleting the program is the user logged in in session data
    if current_user.username != programdata['username']:
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


# route for like program
@dashboard.route('/like-program', methods=['POST'])
@login_required
def like_program():
    # get the program id that we will delete
    programdata = json.loads(request.get_data())
    program_id = programdata['id']

    # this is used to check if user has liked the program... returns true if they have and returns false if they havent

    # get the id of the user
    user_id = current_user.id

    # query the favoriteProgram relationship to see if the user id has liked the program with the id of the entered id.
    user_like = db.session.query(FavoriteProgram).filter(
        (FavoriteProgram.columns.user_id == int(user_id)) & (FavoriteProgram.columns.program_id == program_id)).first()

    # create outcome and add the relationship if the user hasnt liked or remove if they have
    if user_like:
        db.session.query(FavoriteProgram).filter(
            (FavoriteProgram.columns.user_id == int(user_id)) & (FavoriteProgram.columns.program_id == program_id)).delete()
        db.session.commit()
        liked_by_user = False

    else:
        likerelationship = FavoriteProgram.insert().values(
            user_id=(user_id), program_id=(program_id))
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


# program route
@dashboard.route('/program/<int:id>')
@login_required
def program(id):

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
    user_id = current_user.id

    # query the favoriteProgram relationship to see if the user id has liked the program with the id of the entered id.
    user_like = db.session.query(FavoriteProgram).filter(
        (FavoriteProgram.columns.user_id == int(user_id)) & (FavoriteProgram.columns.program_id == int(id))).first()

    if user_like:
        liked_by_user = True
    else:
        liked_by_user = False

    # get amount of likes
    likes = db.session.query(FavoriteProgram).filter(
        (FavoriteProgram.columns.program_id == int(id))).count()

    # render page
    return render_template('program.html', username=current_user.username, program_info=program_info, exercises=exercises, liked_by_user=liked_by_user, likes=likes)


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

    if orderby == 'newest':
        programscreated = programscreated.order_by(
            desc(Program.id)).limit(6).offset(count).all()

    elif orderby == 'oldest':
        programscreated = programscreated.order_by(
            asc(Program.id)).limit(6).offset(count).all()

    elif orderby == 'most_liked':
        programscreated = programscreated.order_by(
            desc(likes_query.c.cnt)).limit(6).offset(count).all()

    elif orderby == 'least_liked':
        programscreated = programscreated.order_by(
            asc(likes_query.c.cnt)).limit(6).offset(count).all()

    else:
        programscreated = programscreated.limit(6).offset(count).all()

    response = make_response(jsonify(to_JSON(programscreated)), 200)
    response.headers["Content-Type"] = "application/json"
    return response
