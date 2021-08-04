from . import db

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))