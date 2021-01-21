
# Modules necessary for flask
from flask import Flask, render_template, request, url_for, redirect, Response

# Import of Novel Crawlers
from novel_crawlers.syosetu import *

# Standard python modules
import time

def book_grab():
    novel_id = "n0649go"
    syo = Novel_Syosetu(novel_id)
    syo.get_meta()
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(syo.get_pages())
    loop.close()
    syo.build_menu()
    syo.post_process()
    syo.build_epub()

app = Flask(__name__)
@app.route("/")
def home():

    return render_template("home.html",
                           message="hey")

@app.route("/",methods=["POST"])
def post():
    text=request.form["u"]
    try:
        book_grab()
    except Exception as error:
        print(error)
    return render_template("home.html")

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


    app.run(debug=True)
