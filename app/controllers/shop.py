from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.user import User
from models.shop import Shop as md_Shop
from models.item import Item
from models import db, serialize

class Shop(Namespace):
    def on_connect(self):
        emit('connect', {'result': 'success'})
    
    @jwt_required()
    def on_open(self):
        username = get_jwt_identity()
        user = User.get(username=username)
        user.shop.open()
        user_to_json = serialize(user, depth=2, avoid=['password', 'items', 'money'])
        emit('open', {'user': user_to_json}, broadcast=True)
    
    @jwt_required()
    def on_close(self):
        username = get_jwt_identity()
        user = User.get(username=username)
        user.shop.close()
        close_room(room=user.id)
        emit('close', {'shop_id': user.shop.id}, broadcast=True)
    
    @jwt_required()
    def on_enter(self, data):
        username = get_jwt_identity()
        room = data.get('room')
        join_room(room)
        items = Item.query.filter_by(user_id=room).all()
        items_to_json = [serialize(item) for item in items]
        emit('enter', {'items': items_to_json})
    
    @jwt_required()
    def on_exit(self, data):
        username = get_jwt_identity()
        room = data.get('room')
        leave_room(room)
        emit('exit', {'result': 'success'})