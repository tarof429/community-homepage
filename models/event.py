from extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    date = db.Column(db.Date)
