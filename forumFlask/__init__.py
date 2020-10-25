from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from forumFlask.config import Config
import os

# this design is so the extension objects doesn't get bond to the application initially
# no app state is stored on the ext obj, so one ext obj can be used fror multiple apps
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
#tell the login extention where the login route is (view function)
login_manager.login_view = 'userBp.login'
#change login alert msg
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import blueprint objects and register them with routes
    from forumFlask.user.view import userBp
    from forumFlask.post.view import postBp
    from forumFlask.page.view import pageBp
    from forumFlask.error.handler import errorBp
    # register
    app.register_blueprint(userBp)
    app.register_blueprint(postBp)
    app.register_blueprint(pageBp)
    app.register_blueprint(errorBp)

    return app