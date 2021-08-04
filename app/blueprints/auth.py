from flask import Blueprint
from controllers.auth import SignIn, Login

auth = Blueprint('auth', __name__, url_prefix='/')
auth.add_url_rule('/sign-in', view_func=SignIn.as_view('sign-in'))
auth.add_url_rule('/login', view_func=Login.as_view('login'))