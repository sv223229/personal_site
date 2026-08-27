
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CachedMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(20), unique=True, nullable=False)
    data = db.Column(db.Text, nullable=False)  # raw JSON stored as text
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CachedMatch {self.match_id}>'

class NameLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<NameLookup {self.id}: {self.name}>'

