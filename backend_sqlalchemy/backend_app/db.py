import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from flask.json import JSONEncoder


app = Flask(__name__)

# CORS
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/WinNBQ.db3'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)

Session(app)


# class CustomJSONEncoder(JSONEncoder):
#
#   def default(o):
#     if type(o) == datetime.timedelta:
#       return str(o)
#     elif type(o) == datetime.datetime:
#       return o.isoformat()
#     else:
#       return super().default(o)
#
#
# app.json_encoder = CustomJSONEncoder


def create_app():
    return app
