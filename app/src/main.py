from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to the too long; automated app!"


# No need to include app.run() here, as Gunicorn will handle running the app
