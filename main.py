#!/usr/bin/env python

from flask import Flask, request, render_template, send_from_directory
from flask_mysqldb import MySQL

from logger import _DEBUG, dlog
from DBDriver import *
from honeywords import *

app = Flask(__name__)

# dbDriver = DBDriver(app, 'localhost', 'root', 'root', 'honeywords')
honeywords = Honeywords(app, open('config.json', 'r'))

@app.route('/')
@app.route('/index')
def index():
    # serve 
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user = request.form['username']
    pwd = request.form['password']
    dlog(user)
    dlog(pwd)
    honeywords.addUser(user, pwd)    
    return render_template("registered.html", username=user, password=pwd)

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    pwd = request.form['password']
    message = honeywords.validateUser(user, pwd)

    if message == honeywords.success_message:
        return render_template("success.html",username=user,password=pwd)
    elif message == honeywords.fail_message:
        return render_template("fail.html",username=user,password=pwd)
    elif message == honeywords.attack_message:
        return render_template("attack.html",username=user,password=pwd)

if __name__ == '__main__':
    app.run(port=8080,debug = True)