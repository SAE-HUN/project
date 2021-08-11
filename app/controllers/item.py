from flask_socketio import Namespace, emit

class Item(Namespace):
    def on_connect(self):
        emit('connect', {'result': 'success'})