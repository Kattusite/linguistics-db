from flask import Flask
import os

app = Flask(__name__)

# Application errors (in production)
# if not app.debug:

from . import routes#, errors
