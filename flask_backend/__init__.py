
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)


if os.getenv("DATABASE_URL") is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


cors = CORS(app)
db = SQLAlchemy(app)


from flask_backend import routes
