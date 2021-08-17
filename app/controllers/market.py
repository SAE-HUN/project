from flask_socketio import Namespace, emit
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from modules.errors import *
from modules.handlers import handle_socket_error
from models.user import User
from models.store import Store


class Market(Namespace):
    @jwt_required()
    def on_open(self, data):
        nickname = get_jwt_identity()
        user = User.query.filter_by(nickname=nickname).first()

        try:
            name = data["name"]
            description = data.get("description", "")
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        try:
            store = Store.create(name, description, user.id)
        except:
            raise SERVER_ERROR()

        response = {
            "result": True,
            "store": {"id": store.id, "name": name, "description": description},
            "user": {"nickname": nickname},
        }
        emit("open", response, broadcast=True)
