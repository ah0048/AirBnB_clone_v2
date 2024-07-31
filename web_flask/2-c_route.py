#!/usr/bin/python3
'''simple script that starts a Flask web application'''
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''hello page'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''hello page'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    '''hello page'''
    return "C {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
