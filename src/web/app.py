"""The app module is the entry point for the Flask web app."""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/index')
def index():
    return '<p>Index</p>'

@app.route('/languages')
def languages():
    return ['English', 'French', 'German']
