# imports
from . import db


# User table database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    programs = db.relationship('Program')


# program table database model
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(3000))


# exercise table database model
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    link = db.Column(db.String(1000))
    Instructions = db.Column(db.String(1000))


# Type table database model
class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150), nullable=False)
    exercise = db.relationship('Exercise')


# FavoriteProgram table database model
FavoriteProgram = db.Table('FavoriteProgram',
                           db.Column('user_id', db.Integer,
                                     db.ForeignKey('user.id')),
                           db.Column('program_id', db.Integer, db.ForeignKey('program.id')))


# ExerciseProgram table database model
ExerciseProgram = db.Table('ExerciseProgram',
                           db.Column('program_id', db.Integer,
                                     db.ForeignKey('program.id')),
                           db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id')))
