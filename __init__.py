from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '243d78185f40265ceaaf892a545d24bccd590190c09401b15ac816ea9cad3104'
app.config['SQLALCHEMY_DATABASE_URI'] =(
    "mysql+pymysql://root:$Trawhats@localhost/foodorder"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from food_ordering_module import routes
