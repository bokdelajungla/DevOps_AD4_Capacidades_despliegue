'''

'''

from server import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    cadenas_ingresadas = db.relationship('Cadena', backref='users')


class Cadena(db.Model):
    __tablename__ = 'cadenas'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    text = db.Column(db.String(100))
    ingresada_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')


class InvalidToken(db.Model):
    __tablename__='invalidtokens'
    id = db.Column(db.Integer, primary_key=True)
    token_body = db.Column(db.String(100))
    pertenece_a = db.Column(db.Integer, db.ForeignKey('users.public_id'))
    user = db.relationship('User')

