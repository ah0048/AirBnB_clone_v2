#!/usr/bin/python3
'''simple script that starts a Flask web application'''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''closes current session'''
    if storage is not None:
        storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb():
    '''sends a page of airbnb clone'''
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
