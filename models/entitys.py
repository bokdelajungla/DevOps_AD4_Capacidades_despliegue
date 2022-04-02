'''

'''

from server import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    children = db.relationship('Cadenas', backref='users')


class Cadena(db.Model):
    __tablename__ = 'cadenas'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    text = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship('Users')


class InvalidToken(db.Model):
    __tablename__='invalidtokens'
    id = db.Column(db.Integer, primary_key=True)
    token_body = db.Column(db.String(100))
    public_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    parent = db.relationship('Users')

