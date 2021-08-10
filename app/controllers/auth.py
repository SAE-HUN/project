from flask.views import View
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from models.user import User

class SignIn(View):
    methods = ['POST']

    def dispatch_request(self):
        params = request.get_json()
        username = params.get('username')
        password = params.get('password')

        user = User.create(username=username, password=password)
        return jsonify(
            result="success",
            access_token = create_access_token(
                identity = username,
                expires_delta = False)
            )

class Login(View):
    methods = ['POST']

    def dispatch_request(self):
        params = request.get_json()
        username = params.get('username')
        password = params.get('password')

        user = User.get(username=username)
        
        if user is not None and user.verify_password(password):
            return jsonify(
                result="success",
                access_token = create_access_token(
                    identity = username,
                    expires_delta = False)
                )
        
        return jsonify(result = "fail")