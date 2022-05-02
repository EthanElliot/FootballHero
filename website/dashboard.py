#imports
from flask import Blueprint, render_template, session, redirect, url_for, abort
from .models import User, Exercise, Type
from .import db

#make flask blueprint 
dashboard = Blueprint('dashboard', __name__)

#dashboard route 
@dashboard.route("/dashboard")
def home():
    #check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


#brouse route 
@dashboard.route("/browse")
def browse():
    #check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('browse.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


#account route 
@dashboard.route("/account")
def account():
    #check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('account.html', username=user)
    else:
        return redirect((url_for('auth.signin')))


#create route 
@dashboard.route("/create")
def create():
    #check if user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('create.html', username=user)
    else:
        return redirect((url_for('auth.signin')))



#exercise route 
@dashboard.route('/exercise/<int:id>')
def exercise(id):
    #check if user is logged in
    if 'user' in session:
        user = session['user']
        #query the database for exercise with the id in the route
        exercise = db.session.query(Exercise, Type).join(Type).filter(Exercise.id == id).first()
        #if exercise exists render the page
        if exercise: 
            print(exercise)
            return render_template('exercise.html', exercise=exercise)
        #if exercise doesnt exist return a error   
        else:
            abort(404)  
    else:
        return redirect((url_for('auth.signin')))
