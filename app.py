from flask import Flask, request, jsonify, render_template, abort
from datetime import datetime, timedelta
import random, string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def home():
    return render_template("index.html")

