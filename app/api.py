# Define Flask API endpoints

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Traffic Simulation API"