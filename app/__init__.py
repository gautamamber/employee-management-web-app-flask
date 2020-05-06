# third party imports

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


# local imports
from app import models
from .admin import admin as admin_blueprint
from .auth import auth as auth_blueprint
from .home import home as home_blueprint
from config import app_config
from messages import ApplicationMessages

# db variable initialize

db = SQLAlchemy()

# Login manager object  initialization

login_manager = LoginManager()


def create_app(config_name):
    """
    Initialize application with env
    :param config_name:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = ApplicationMessages.MUST_BE_LOGIN
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(auth_blueprint)
    return app
