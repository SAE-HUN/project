from flask import jsonify


def handle_error(e):
    return jsonify(title=e.title), e.code
