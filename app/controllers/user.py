from flask import request, jsonify
from flask.views import View, MethodView

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

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


class Login(View):
    methods = ["POST"]

    def dispatch_request(self):
        if not request.is_json:
            raise NO_JSON_CONTENT()

        try:
            params = request.get_json()
            username = params["username"]
            password = params["password"]
        except KeyError:
            raise NO_REQUIRED_PARAMS()

        user = UserMD.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return jsonify(access_token=create_access_token(username)), 200
        else:
            raise LOGIN_FAIL()
