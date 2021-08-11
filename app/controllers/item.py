from flask_socketio import Namespace, emit
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import serialize
from models.item import Item as md_Item
from models.user import User

class Item(Namespace):
    def on_connect(self):
        emit('connect', {'result': 'success'})
    
    def on_get_items(self, data):
        room = data['room']
        items = md_Item.get_items(room)
        items_to_json = [serialize(item) for item in items]
        emit('get_items', {'items': items_to_json})
    
    @jwt_required()
    def on_buy(self, data):
        buyer_username = get_jwt_identity()
        item = data['item']
        buyer = User.get(username=buyer_username)
        result = buyer.buy(item)
        
        if result['result'] == 'success':
            emit('buy', {'result': 'success', 'item': item}, namespace='/shops', to=result['seller'])
        else:
            emit('buy', {'result': 'fail', 'reason': result['reason']})