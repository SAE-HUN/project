from flask import Flask
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

from models import db
from blueprints.auth import auth
from controllers.shop import Shop as ns_shop
from controllers.item import Item

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
jwt = JWTManager(app)
db.init_app(app)

app.config.from_envvar('APP_CONFIG_FILE')

with app.app_context():
    from models import user, shop, item
    db.create_all()

app.register_blueprint(auth)
socketio.on_namespace(ns_shop('/shops'))
socketio.on_namespace(Item('/items'))

if __name__ == '__main__':
    socketio.run(app)