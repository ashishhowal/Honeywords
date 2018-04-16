#!/usr/bin/env python

from flask import Flask, request, render_template
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
    # cur, rs = dbDriver._exec('''SHOW TABLES''')
    honeywords.addUser('swappy','bird')
    return "Pls work"

@app.route('/login')
def login():
    print honeywords.validateUser('swappy','bird')
    print honeywords.validateUser('swappy','lol')
    print honeywords.validateUser('swappy','201590')
    return "Login Page"

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return

if __name__ == '__main__':
    app.run(port=8080)