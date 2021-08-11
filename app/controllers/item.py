from flask_socketio import Namespace

class Item(Namespace):
    def on_hello(self):
        print('hello, Item')