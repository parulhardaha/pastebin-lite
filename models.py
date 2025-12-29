from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

#table
class Paste(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    max_views = db.Column(db.Integer, nullable=True)
    current_views = db.Column(db.Integer, default=0)
