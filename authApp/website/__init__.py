import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mysqldb import MySQLdb
from flask_migrate import Migrate

db = SQLAlchemy()
# DB_NAME = "database.db"
DB_NAME = 'flaskTest'

def creat_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://user:password@localhost/{DB_NAME}'

    db.init_app(app)
    
    # for migrating database
    migrate = Migrate(app, db)

    #FOR IMPORTING 
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Employee
    create_database(app)

    #LOGIN MANAGER
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
