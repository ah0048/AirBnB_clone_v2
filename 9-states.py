#!/usr/bin/python3
'''simple script that starts a Flask web application'''
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''closes current session'''
    if storage is not None:
        storage.close()


@app.route('/states', strict_slashes=False)
def state_list():
    '''sends a page of states list'''
    states_list = storage.all(State).values()
    states_list = sorted(states_list, key=lambda state: state.name)
    return render_template('9-states.html', states_list=states_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
