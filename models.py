from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_type = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    priority_level = db.Column(db.String(10), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False, default='not completed')

