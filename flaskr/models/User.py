from . import db
from .Shop import Shop
from .Item import Item

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    money = db.Column(db.Integer, default=0, nullable=False)
    shop = db.relationship(Shop, backref='user', uselist=False)
    items = db.relationship(Item, backref='user')