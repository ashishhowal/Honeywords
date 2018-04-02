#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, I am flask."

if __name__ == '__main__':
    app.run()
