from flask import Flask;
from flask import render_templates
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    return 'login'; 