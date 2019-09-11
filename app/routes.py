from . import app, lingdb_client, querier, query
from lingdb.exceptions import QuorumError
from data import const
from flask import render_template, redirect, request, url_for, flash
import json, traceback

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == 'POST':


    # Handle normal GET requests
    return render_template('front.html')

@app.route('/index.html')
def index():
    return redirect('/')

@app.route('/index')
def index1():
    return redirect('/')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/survey.html')
def survey1():
    return redirect('/survey')

@app.route('/about')
def about():
    return render_template('about.html')
