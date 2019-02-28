from . import app, lingdb_client
from lingdb.exceptions import QuorumError
from data import const
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

        # By default, we will be returning info to the user (blue message box)
        retCode = const.INFO

        # Send all queries to client for processsing
        try:
            ret = lingdb_client.handleQueries(queries, listMode=listMode, dataset=dataset)

        # Not enough data to answer this query. Inform user
        except QuorumError:
            ret = "".join([
                '<span class=quote>',
                '"There is as yet insufficient data for a meaningful answer."',
                '</span><br>',
                '<span class=quoteattrib> -- Isaac Asimov, 1956 </span>',
                '<br><br>',
                'Please check back later once more data has been gathered!'
            ])
            retCode = const.WARN

        # Inform the user that a server error occurred, and log the error.
        except:
            ret = "Sorry, an unknown server error occurred! Please let the developer know how you got this message so they can fix it."
            retCode = const.DANGER
            traceback.print_exc()

        # Return the status code and response payload to the frontend for display to user
        return json.dumps({const.RET_CODE: retCode, const.PAYLOAD: ret})

    # Handle normal GET requests
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
