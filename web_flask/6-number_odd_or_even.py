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
    '''hbnb page'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    '''c page'''
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    '''python page'''
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    '''number page'''
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    '''number page'''
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    '''number page'''
    if int(n) % 2 == 0:
        state = 'even'
    else:
        state = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, state=state)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
