from models.databaseInit import db
from utils.encoder import encodePassword


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = encodePassword(password)

    def __repr__(self):
        return '<User %r>' % self.username
