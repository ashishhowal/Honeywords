#!/usr/bin/env python

from flask import Flask, request
from flask_mysqldb import MySQL

from logger import _DEBUG, dlog
from DBDriver import *

app = Flask(__name__)

dbDriver = DBDriver(app, 'localhost', 'root', 'root', 'test')

@app.route('/')
@app.route('/index')
def index():
    cur, rs = dbDriver._exec('''SHOW TABLES''')
    return str(cur.fetchall())

@app.route('/login')
def login():
    return "Login Page"

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return

if __name__ == '__main__':
    app.run(port=8080)