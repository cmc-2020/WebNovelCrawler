from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



# run app: start with `python app.py` and open the link in your browser
if __name__ == "__main__":

    # This allows the program to be debugged in real time.
    app.run(debug=True)