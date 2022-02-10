from flask import Flask, request, render_template
from connection import connect_rds, connect_redshift

app = Flask(__name__)

@app.route('/login', methods=['GET, POST'])
def query_login():
    return {}

@app.route('/disclaimer', methods=['POST'])
def query_disclaimer():
    return render_template('disclaimer.html');

@app.route('/startregistration', methods=['POST'])
def query_startregistration():
    return render_template('register.html');


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')
    #return render_template('index.html')
