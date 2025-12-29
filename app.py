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

# Create paste (POST)
@app.route("/paste", methods=["POST"])
def create_paste():
    data = request.get_json() if request.is_json else request.form

    content = data.get("content")
    ttl = data.get("ttl")
    max_views = data.get("max_views")

    if not content:
        return jsonify({"error": "Content required"}), 400

    paste_id = generate_id()

    expires_at = None
    if ttl:
        try:
            expires_at = datetime.utcnow() + timedelta(seconds=int(ttl))#adds that time difference to the current UTC time giving the exact expiration time
        except:
            return jsonify({"error": "Invalid TTL value"}), 400

    paste = Paste(
        id=paste_id,
        content=content,
        expires_at=expires_at,
        max_views=int(max_views) if max_views else None
    )

    db.session.add(paste)
    db.session.commit()

    #request.host_url-gets the base URL of  server
    url = request.host_url + "paste/" + paste_id

    #if json then return json
    if request.is_json:
        return jsonify({"url": url}), 201

    return render_template("view.html", url=url)

#view paste (GET)
@app.route("/paste/<paste_id>", methods=["GET"])
def view_paste(paste_id):
    paste = Paste.query.get_or_404(paste_id)

    if is_expired(paste):
        abort(404)

    paste.current_views += 1
    db.session.commit()

    if request.headers.get("Accept") == "application/json":
        return jsonify({"content": paste.content})

    return render_template("view.html", content=paste.content)


if __name__ == "__main__":
    app.run(debug=True)




   
