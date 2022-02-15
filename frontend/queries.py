from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/main', methods=['POST'])
def query_main():
    return render_template('main.html');

@app.route('/login', methods=['POST'])
def query_login():
    return render_template('login.html');

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
