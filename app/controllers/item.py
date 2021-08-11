from flask_socketio import Namespace, emit

from models import serialize
from models.item import Item as md_Item

class Item(Namespace):
    def on_connect(self):
        emit('connect', {'result': 'success'})
    
    def on_get_items(self, data):
        room = data['room']
        items = md_Item.get_items(room)
        items_to_json = [serialize(item) for item in items]
        emit('get_items', {'items': items_to_json})