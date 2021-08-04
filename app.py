from flask import Flask

app = Flask(__name__)

def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/')
hello_world