# imports
from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeSerializer
from flask_login import LoginManager

# db variables
db = SQLAlchemy()
DB_NAME = 'FootballHero.db'

# create a Url Serializer
s = URLSafeSerializer(secrets.token_urlsafe(32))

# set up flask mail
mail = Mail()

# set up db migration
migrate = Migrate()

login_manager = LoginManager()


# create flask app function
def create_app():
    # configure the flask app and secret keys
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
    app.config['DEBUG'] = True

    # set up flask mail
    app.config.from_pyfile('config.cfg')
    mail.init_app(app)

    # set up database
    migrate.init_app(app, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Set up flask login
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    # import the db models
    from .views import views
    from .auth import auth
    from .dashboard import dashboard
    from .models import User, Program, Exercise, Type, FavoriteProgram, ExerciseProgram

    # configue login user
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # redgister the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')

    # create db
    create_database(app)

    # return app
    return app


# database creation function
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')
