from . import db


class TradeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(64))
    category = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)

    def create(name, description, category, price, user_id, store_id):
        item = TradeItem(
            name=name,
            description=description,
            category=category,
            price=price,
            user_id=user_id,
            store_id=store_id,
        )
        db.session.add(item)
        db.session.commit()

        return item
    
    def update(self, name, description, category, price):
        self.name = name
        self.description = description
        self.categor = category
        self.price = price
        db.session.commit()
