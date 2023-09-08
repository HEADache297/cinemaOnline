from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = "qwe"
app.secret_key = 'fff'
app.app_context().push()
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=1)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cinemaOnline.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

# users = Save()
# users.read()
