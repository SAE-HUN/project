from datetime import datetime

from . import db


class TradeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now())
    item_id = db.Column(db.Integer, db.ForeignKey("trade_item.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def create(item_id, buyer_id, seller_id):
        history = TradeHistory(
            item_id=item_id,
            buyer_id=buyer_id,
            seller_id=seller_id,
        )
        db.session.add(history)
