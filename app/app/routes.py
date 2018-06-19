from . import app
from flask import render_template, redirect, request, url_for, flash
from . import lingdb_client

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == 'POST':
        # time = request.form['timestamp']
        # results = course_search.course_db_query(query, semester)
        # returnObj = {"results": results, "time":time}
        # return str(returnObj)
        f = request.form
        result = str(lingdb_client.handleQuery(f))
        reply = "..."
        return result + " " + reply
    return render_template('front.html')

@app.route('/index.html')
def index():
    return redirect('/')

@app.route('/index')
def index1():
    return redirect('/')
