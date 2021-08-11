from . import db, commit

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def create(name, price, user_id):
        item = Item(name=name, price=price, user_id=user_id)
        commit(item)
        return item