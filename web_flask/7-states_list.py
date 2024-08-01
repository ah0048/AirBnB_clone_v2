#!/usr/bin/python3
'''simple script that starts a Flask web application'''
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    '''sends a page of states list'''
    states_list = storage.all(State).values()
    states_list = sorted(states_list, key=lambda state: state.name)
    return render_template('7-states_list.html', states_list=states_list)


@app.teardown_appcontext
def teardown_db(exception):
    '''closes current session'''
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
