from werkzeug.exceptions import HTTPException


class NO_JSON_CONTENT(HTTPException):
    code = 400
    title = "NO_JSON_CONTENT"


class NO_REQUIRED_PARAMS(HTTPException):
    code = 400
    title = "NO_REQUIRED_PARAMS"


class EXIST_NICKNAME(HTTPException):
    code = 400
    title = "EXIST_NICKNAME"


class EXIST_USERNAME(HTTPException):
    code = 400
    title = "EXIST_USERNAME"


class SERVER_ERROR(HTTPException):
    code = 500
    title = "SERVER_ERROR"
