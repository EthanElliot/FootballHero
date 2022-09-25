# imports
from . import db
from flask_login import UserMixin


# FavoriteProgram table database model
FavoriteProgram = db.Table(
    'FavoriteProgram',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id')
    ),
    db.Column(
        'program_id',
        db.Integer,
        db.ForeignKey('program.id')
    )
)


# ExerciseProgram table database model
ExerciseProgram = db.Table(
    'ExerciseProgram',
    db.Column(
        'program_id',
        db.Integer,
        db.ForeignKey('program.id')
    ),
    db.Column(
        'exercise_id',
        db.Integer,
        db.ForeignKey('exercise.id')
    )
)


# User table database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    verified = db.Column(db.Boolean, default=False)

    programs = db.relationship('Program')
    favorites = db.relationship(
        'Program',
        secondary=FavoriteProgram,
        backref=db.backref('favoriteprograms'),
        lazy='dynamic'
    )


# program table database model
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(3000))
    exercises = db.relationship(
        'Exercise',
        secondary=ExerciseProgram,
        backref='exercises'
    )
    favorited = db.relationship(
        'User',
        secondary=FavoriteProgram,
        backref=db.backref('favirouted'),
        lazy='dynamic'
    )


# exercise table database model
class Exercise(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    Instructions = db.Column(db.String(1000))

# Type table database model


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150), nullable=False)
    exercise = db.relationship('Exercise')
