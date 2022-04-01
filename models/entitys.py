from server import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    children = db.relationship('Cadenas', backref='users')

class Cadenas(db.Model):
    __tablename__ = 'cadenas'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    text = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship('Users')
