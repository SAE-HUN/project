from flask import jsonify, request
from flask_socketio import emit


def handle_error(e):
    return jsonify(title=e.title), e.code


def handle_socket_error(e):
    emit(request.event["message"], {"result": False, "title": e.title})
