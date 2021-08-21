from flask_socketio import Namespace, emit, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.store import Store as StoreMD
from models.trade_item import TradeItem
from models.trade_history import TradeHistory
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

        items = store.trade_item
        response = {"result": True, "items": []}
        for i in range(len(items)):
            item = items[i]
            if item.is_selled:
                continue
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

    @jwt_required()
    def on_modify(self, data):
        nickname = get_jwt_identity()
        user = User.query.filter_by(nickname=nickname).first()

        try:
            item_id = data["id"]
            name = data["name"]
            description = data.get("description", "")
            category = data["category"]
            price = data["price"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        item = TradeItem.query.get(item_id)
        if item is None or item.is_selled:
            raise NO_EXIST_ITEM()

        if user != item.owner:
            raise NO_AUTHORIZATION()

        try:
            item.update(name, description, category, price)
        except:
            raise SERVER_ERROR()

        response = {
            "result": True,
            "item": {
                "id": item_id,
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "user": {"nickname": nickname},
                "store": {"id": item.store.id},
            },
        }
        emit("modify", response, to=item.store.id)

    @jwt_required()
    def on_delete(self, data):
        nickname = get_jwt_identity()
        user = User.query.filter_by(nickname=nickname).first()

        try:
            item_id = data["id"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        item = TradeItem.query.get(item_id)
        if item is None or item.is_selled:
            raise NO_EXIST_ITEM()

        if item.store is None:
            raise NO_EXIST_STORE()

        if user != item.owner:
            raise NO_AUTHORIZATION()

        try:
            item.delete()
        except:
            raise SERVER_ERROR()

        response = {
            "result": True,
            "item": {
                "id": item_id,
                "user": {"nickname": item.owner.nickname},
                "store": {"id": item.store.id},
            },
        }
        emit("delete", response, to=item.store.id)

    @jwt_required()
    def on_trade(self, data):
        nickname = get_jwt_identity()
        buyer = User.query.filter_by(nickname=nickname).first()

        try:
            item_id = data["id"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        item = TradeItem.query.get(item_id)
        if item is None or item.is_selled:
            raise NO_EXIST_ITEM()

        seller = item.owner
        store = item.store

        if buyer.money < item.price:
            raise NOT_ENOUGH_MONEY()

        if store is None:
            raise NO_EXIST_STORE()

        try:
            TradeHistory.create(item.id, buyer.id, seller.id)
            buyer.buy(item.price)
            seller.sell(item.price)
            item.delete()
        except:
            raise SERVER_ERROR()

        response = {
            "result": True,
            "seller": {"nickname": seller.nickname},
            "buyer": {"nickname": buyer.nickname},
            "item": {"id": item_id},
        }
        emit("trade", response, to=store.id)

    def on_exit(self, data):
        try:
            store_id = data["id"]
        except:
            raise NO_REQUIRED_PARAMS()

        leave_room(store_id)
        emit("exit", {"result": True, "store": {"id": store_id}})
