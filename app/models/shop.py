from . import db, commit

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_opend_shops():
        shops = Shop.query.filter_by(is_open=True).all()
        return shops
    
    def get(shop_id):
        shop = Shop.query.get(shop_id)
        return shop
    
    def open(self):
        self.is_open = True
        commit(self)
    
    def close(self):
        self.is_open = False
        commit(self)