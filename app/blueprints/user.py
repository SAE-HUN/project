from flask import Blueprint

from controllers.user import User
from errors.user import *
from errors.handlers import handle_error

bp = Blueprint("user", __name__, url_prefix="/users/")
bp.add_url_rule("/", view_func=User.as_view("user"))


bp.register_error_handler(NO_JSON_CONTENT, handle_error)
bp.register_error_handler(NO_REQUIRED_PARAMS, handle_error)
bp.register_error_handler(EXIST_NICKNAME, handle_error)
bp.register_error_handler(EXIST_USERNAME, handle_error)
bp.register_error_handler(SERVER_ERROR, handle_error)
