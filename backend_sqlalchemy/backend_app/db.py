import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from flask.json import JSONEncoder


app = Flask(__name__)


def manage_sensitive(name):
    v1 = os.getenv(name)

    secret_fpath = f'/run/secrets/{name}'
    existence = os.path.exists(secret_fpath)

    if v1 is not None:
        return v1

    if existence:
        v2 = open(secret_fpath).read().rstrip('\n')
        return v2

    if all([v1 is None, not existence]):
        return KeyError(f'{name}')


# CORS
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/WinNBQ.db3'
app.config['SECRET_KEY'] = manage_sensitive('FLASK_SECRET_KEY')
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
