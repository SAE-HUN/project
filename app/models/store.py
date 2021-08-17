from . import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def create(name, description, user_id):
        store = Store(name=name, description=description, user_id=user_id)
        db.session.add(store)
        db.session.commit()

        return store
    
    def update(self, name, description):
        self.name = name
        self.description = description
        db.session.commit()
