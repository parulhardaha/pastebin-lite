from flask import Flask, request, jsonify, render_template, abort, render_template
from datetime import datetime, timedelta
import random, string
from models import db, Paste
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  #creates all tables from models.py

#generate unique ID
def generate_id():
    while True:
        pid = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not Paste.query.get(pid):
            return pid

#check if paste is expired or views exceeded
def is_expired(paste):
    if paste.expires_at and datetime.utcnow() > paste.expires_at:
        return True
    if paste.max_views is not None and paste.current_views >= paste.max_views:
        return True
    return False

# home
@app.route("/")
def home():
    return render_template("index.html")



   
