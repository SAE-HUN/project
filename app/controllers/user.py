from flask import request, jsonify
from flask.views import MethodView

from flask_jwt_extended import create_access_token

from models.user import User as UserMD
from errors.user import *


class User(MethodView):
    def post(self):
        if not request.is_json:
            raise NO_JSON_CONTENT()

        try:
            params = request.get_json()
            username = params["username"]
            password = params["password"]
            nickname = params["nickname"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        if not UserMD.check_nickname(nickname):
            raise EXIST_NICKNAME()

        if not UserMD.check_username(username):
            raise EXIST_USERNAME()

        try:
            user = UserMD.create(username, password, nickname)
        except:
            raise SERVER_ERROR()

        response = jsonify(access_token=create_access_token(nickname))
        return response, 201
