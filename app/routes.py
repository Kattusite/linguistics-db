from . import app, lingdb_client
from flask import render_template, redirect, request, url_for, flash
import json

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == 'POST':
        # Extract the payload from the request form
        f = request.form
        data = json.loads(f["payload"])
        listMode = True if f["listMode"].lower() == "true" else False
        # data is a list of query dicts, each containing:
        # "consonants" -> A (stringified) list of the consonants to query
        # "vowels"     -> A (stringified) list of the vowels to query
        # "k"          -> A (stringified) int of how many matches to find
        # "mode"       -> A string of which comparison mode to apply to k
        # "syllable"   -> A string of a syllable structure to query
        # "classes"    -> A (stringified) list of which metaclasses to query

        # Parse the boolean string to a proper bool

        # Send all queries to client for processsing
        ret = lingdb_client.handleQueries(data, listMode=listMode)
        return ret
    return render_template('front.html')

@app.route('/index.html')
def index():
    return redirect('/')

@app.route('/index')
def index1():
    return redirect('/')
