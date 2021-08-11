from . import db, commit

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    want_sell = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def create(name, price, user_id):
        item = Item(name=name, price=price, user_id=user_id)
        commit(item)
        return item
    
    def update(self, data):
        for column, value in data.items():
            setattr(self, column, value)
        
        commit(self)

    def get_items(user_id, want_sell):
        return Item.query.filter_by(user_id=user_id, want_sell=want_sell).all()