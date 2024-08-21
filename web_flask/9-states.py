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
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    '''sends a page of states list'''
    states = storage.all(State).values()
    state = None
    if id is None:
        return render_template('9-states.html', states=states, state=None)
    else:
        for state_req in states:
            if state_req.id == id:
                state = state_req
        if state is None:
            return render_template('9-states.html', states=None, state=None)
        else:
            return render_template('9-states.html', states=None, state=state)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
