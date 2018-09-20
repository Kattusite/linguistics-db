from . import app, lingdb_client
from flask import render_template, redirect, request, url_for, flash
import json

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == 'POST':
        # time = request.form['timestamp']
        # results = course_search.course_db_query(query, semester)
        # returnObj = {"results": results, "time":time}
        # return str(returnObj)
        f = request.form
        data = json.loads(f["payload"])

        # TODO Change verbose to a boolean like a normal person.
        listMode = (f["listMode"]) == "true")

        # TODO I think this whole block is deprecated -- remove if so
        # TODO: result, reply get overwritten at each step
        #for query in data:
        #    result = str(lingdb_client.handleQuery(query))
        #    reply = query["reply"]
        ret = lingdb_client.handleQueries(data, verbose)
        return ret
        # return result + " languages " + reply
    return render_template('front.html')

@app.route('/index.html')
def index():
    return redirect('/')

@app.route('/index')
def index1():
    return redirect('/')
