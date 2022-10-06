from flask import render_template, redirect, request

from . import app, querier, responder

@app.route("/", methods = ["GET", "POST"])
def main():
    # Handle POST requests, which include queries for the DB
    if request.method == 'POST':

        # Build queries from request
        queries = querier.queriesFromRequest(request)
        db = querier.dbFromRequest(request)

        # Ask querier to run the query against the DB, and generate HTML response
        HTML = ""
        status = ""
        results = None
        graphData = None
        try:
            print("handling queries...")
            results = querier.handleQueries(queries, db)
            print("obtaining graph data...")
            graphData = querier.graphData(results[0])
            print("graph data:", graphData)
            print("generating HTML...")
            HTML = responder.generateHTML(results)
            status = responder.INFO
        except querier.QuorumError as err:
            HTML = responder.quorumErrorHTML(err)
            status = responder.WARN
            print(err)
        except Exception as err:
            HTML = responder.serverErrorHTML(err)
            status = responder.DANGER
            print(err)

        return responder.respond(HTML, status, data=graphData)

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
