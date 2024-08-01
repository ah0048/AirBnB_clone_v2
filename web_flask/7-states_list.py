#!/usr/bin/python3
'''simple script that starts a Flask web application'''
from flask import Flask, render_template
from models import storage


storage.all()
app = Flask(__name__)






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
