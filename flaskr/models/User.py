from . import db
from .shop import Shop
from .item import Item

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    money = db.Column(db.Integer, default=0, nullable=False)
    shop = db.relationship(Shop, backref='user', uselist=False)
    items = db.relationship(Item, backref='user')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.shop = Shop()
    
    def create(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def find(username, password):
        user = User.query.filter_by(username=username, password=password).first()
        return user