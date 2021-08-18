from flask_socketio import Namespace, emit, join_room
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.store import Store as StoreMD
from models.trade_item import TradeItem
from modules.errors import *


class Store(Namespace):
    def on_enter(self, data):
        try:
            store_id = data["store_id"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        store = StoreMD.query.get(store_id)
        if store is None:
            raise NO_EXIST_STORE()

        join_room(store_id)
        emit("enter", {"result": True, "store": {"id": store_id}})

    @jwt_required()
    def on_register(self, data):
        nickname = get_jwt_identity()
        user = User.query.filter_by(nickname=nickname).first()

        try:
            name = data["name"]
            description = data.get("description", "")
            price = data["price"]
            category = data["category"]
            store_id = data["store_id"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        store = StoreMD.query.get(store_id)
        if store is None:
            raise NO_EXIST_STORE()

        try:
            item = TradeItem.create(
                name, description, category, price, user.id, store.id
            )
        except:
            raise SERVER_ERROR()

        serialized_item = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
        }
        serialized_user = {"nickname": nickname}
        serialized_store = {"id": store_id}
        emit(
            "register",
            {
                "result": True,
                "user": serialized_user,
                "store": serialized_store,
                "item": serialized_item,
            },
            to=store_id,
        )

    def on_list(self, data):
        store_id = data["store_id"]
        store = StoreMD.query.get(store_id)
        if store is None:
            raise NO_EXIST_STORE()

        items = TradeItem.query.filter_by(store_id=store.id).all()
        response = {"result": True, "items": []}
        for i in range(len(items)):
            item = items[i]
            serialized_user = {"nickname": item.owner.nickname}
            serialized_store = {"id": item.store.id}
            serialized_item = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "category": item.category,
                "user": serialized_user,
                "store": serialized_store,
            }
            response["items"].append(serialized_item)
        emit("list", response)
