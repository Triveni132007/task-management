from config.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True, nullable=False )
    password = db.Column(db.String(300), nullable=False)

    task = db.relationship("Task", backref="user", lazy=True)