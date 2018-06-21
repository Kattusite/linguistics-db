from flask import Flask
import os
# Email error logs
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)

# Application errors (in production)
# if not app.debug:


from . import routes#, errors
