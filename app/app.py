from flask import Flask, request

from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit

from blueprints import user
from controllers.market import Market
from controllers.store import Store
from models import db
from modules.handlers import handle_socket_error

app = Flask(__name__)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")


socketio.on_error("/market")(handle_socket_error)
socketio.on_error("/store")(handle_socket_error)


app.config["SECRET_KEY"] = "1234"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///C:/Users/fjdks/project/app/db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

app.register_blueprint(user.bp)
socketio.on_namespace(Market("/market"))
socketio.on_namespace(Store("/store"))

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    socketio.run(app=app, debug=True)
