from enum import Enum


class ErrorCode(Enum):
    USER_NOT_FOUND = {"code": 404, "detail": "USER_NOT_FOUND", "description": "The user does not exist"}
    USER_EXIST = {"code": 409, "detail": "USER_EXIST", "description": "The user already exists"}
    UNAUTHORIZED = {"code": 401, "detail": "UNAUTHORIZED", "description": "Invalid credentials"}
    BAD_FORMAT_PASSWORD = {"code": 400, "detail": "BAD_FORMAT_PASSWORD", "description": "The password format is invalid"}

    def __init__(self, details):
        self.code = details["code"]
        self.message = details["detail"]
        self.description = details["description"]
