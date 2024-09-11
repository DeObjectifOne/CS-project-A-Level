from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#creation of the database
db = SQLAlchemy()
DB_NAME = "database.db"

#used to both instantiate flask + creating a secret key for the website
def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #used to import code from auth.py and views.py
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Task

    with app.app_context():
          db.create_all()
         
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
          print("Database has been initialized")