from werkzeug.security import generate_password_hash

from . import db, commit
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
        self.password = generate_password_hash(password)
        self.shop = Shop()
    
    def create(username, password):
        user = User(username=username, password=password)
        commit(user)
        
        return user
    
    def get(username):
        user = User.query.filter_by(username=username).first()
        return user
    
    def buy(self, item_id):
        item = Item.query.get(item_id)
        seller = item.user

        if not seller.shop.is_open:
            return {'result': 'fail', 'reason': 'not open shop'}
        
        if self.money < item.price:
            return {'result': 'fail', 'reason': 'not enough money'}

        seller.money += item.price
        self.money -= item.price
        item.user = self
        commit([self, seller, item])
        return {'result': 'success'}