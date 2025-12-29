from flask import Flask, request, jsonify, render_template, abort, render_template
from datetime import datetime, timedelta
import random, string
from models import db, Paste
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")





   
