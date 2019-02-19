from . import app, lingdb_client
from flask import render_template, redirect, request, url_for, flash
import json, traceback

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == 'POST':
        # Extract the payload from the request form
        f = request.form
        queries = json.loads(f["payload"])
        listMode = (f["listMode"].lower() == "true")
        # queries is a list of query dicts, each containing:
        # "consonants" -> A (stringified) list of the consonants to query
        # "vowels"     -> A (stringified) list of the vowels to query
        # "k"          -> A (stringified) int of how many matches to find
        # "mode"       -> A string of which comparison mode to apply to k
        # "syllable"   -> A string of a syllable structure to query
        # "classes"    -> A (stringified) list of which metaclasses to query

        # Specify which language dataset to use
        dataset = f["dataset"]

        # Send all queries to client for processsing
        try:
            ret = lingdb_client.handleQueries(queries, listMode=listMode, dataset=dataset)
        # Inform the user that a server error occurred, and log the error.
        except:
            ret = "Sorry, an unknown server error occurred! If you're seeing this please let the developer know how you got this message so they can fix it."
            traceback.print_exc()
        return ret
    return render_template('front.html')

@app.route('/index.html')
def index():
    return redirect('/')

@app.route('/index')
def index1():
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')
