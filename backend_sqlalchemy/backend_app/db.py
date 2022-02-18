import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

# CORS
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/WinNBQ.db3'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db = SQLAlchemy(app)


def create_app():
    return app
