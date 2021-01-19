
# Modules necessary for flask
from flask import Flask, render_template, request, url_for, redirect, Response

# Import of Novel Crawlers
from novel_crawlers.syosetu import *

# Standard python modules
import time

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("home.html",
                           message="hey")

# Generates the progress of the books loading time
@app.route('/progress')
def progress():

    def generate():
        x = 100

        # yields the progress of x
        yield "data:" + str(x) + "\n\n"



    return Response(generate(), mimetype='text/event-stream')


# run app: start with `python app.py` and open the link in your browser
if __name__ == "__main__":

    # This allows the program to be debugged in real time.
    app.run(debug=True)