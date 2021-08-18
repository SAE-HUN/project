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


class LOGIN_FAIL(HTTPException):
    code = 400
    title = "LOGIN_FAIL"


class NO_EXIST_STORE(HTTPException):
    code = 404
    title = "NO_EXIST_STORE"


class NO_AUTHORIZATION(HTTPException):
    code = 403
    title = "NO_AUTHORIZATION"


class NO_EXIST_ITEM(HTTPException):
    code = 404
    title = "NO_EXIST_ITEM"
