"""The app module is the entry point for the Flask web app."""

from flask import (
    Flask,
    request,
)
from flask.json.provider import DefaultJSONProvider

from lingdb.dataset import Dataset
from web.handlers import LanguageHandler

# Allow UTF-8 characters in JSON replies
DefaultJSONProvider.ensure_ascii = False
DefaultJSONProvider.sort_keys = False

app = Flask(__name__)


@app.route('/')
def root():
    """Return the main application homepage."""
    return '<p>Index</p>'


@app.route("/hello")
def hello_world():
    """Return a simple hello world message."""
    return "<p>Hello, World!</p>"


language_handler = LanguageHandler()


@app.route('/languages')
def languages():
    """Return information about the requested set of languages as a JSON API response."""
    return language_handler.handle(request)

@app.route('/datasets')
def datasets():
    """Return a list of the available language datasets."""
    return [dataset for dataset in Dataset if not dataset.is_test()]
