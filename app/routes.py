from . import app, querier, query, responder
# from lingdb.exceptions import QuorumError
from data import const
from flask import render_template, redirect, request, url_for, flash
import json, traceback

@app.route("/", methods = ["GET", "POST"])
def main():
    # Handle POST requests, which include queries for the DB
    if request.method == 'POST':

        # Build queries from request
        queries = querier.queriesFromRequest(request)

        # Ask querier to run the query against the DB, and generate HTML response
        HTML = ""
        status = ""
        try:
            results = querier.handleQueries(queries)
            HTML = responder.generateHTML(results)
            status = responder.INFO
        except QuorumError:
            HTML = responder.QuorumErrorHTML() # TODO
            status = responder.WARN
        except Exception as err:
            HTML = responder.ServerErrorHTML() # TODO
            status = responder.DANGER

        return responder.respond(HTML, status)

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
