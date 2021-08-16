from werkzeug.security import generate_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(32), unique=True, nullable=False)
    money = db.Column(db.Integer, default=0)

    def create(username, password, nickname):
        user = User(
            username=username,
            password=generate_password_hash(password),
            nickname=nickname,
        )
        db.session.add(user)
        db.session.commit()

    def check_nickname(nickname):
        result = User.query.filter_by(nickname=nickname).first()
        return True if result is None else False

    def check_username(username):
        result = User.query.filter_by(username=username).first()
        return True if result is None else False
