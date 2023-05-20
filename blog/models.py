# blog/models.py
from . import db
import datetime

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __init__(self, title, content, date, image):
        self.title = title
        self.content = content
        self.date = date
        self.image = image

    def __repr__(self):
        return f"Post(title='{self.title}', date='{self.date}')"


