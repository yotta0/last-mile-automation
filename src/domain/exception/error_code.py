from enum import Enum


class ErrorCode(Enum):
    USER_NOT_FOUND = {"code": 404, "detail": "USER_NOT_FOUND", "description": "The user does not exist"}
    ATTENDANCE_NOT_FOUND = {"code": 404, "detail": "ATTENDANCE_NOT_FOUND", "description": "The attendance does not exist"}
    ATTENDANCE_ALREADY_DELETED = {"code": 409, "detail": "ATTENDANCE_ALREADY_DELETED", "description": "The attendance is already deleted"}
    GREEN_ANGEL_NOT_FOUND = {"code": 404, "detail": "GREEN_ANGEL_NOT_FOUND", "description": "The green angel does not exist"}
    GREEN_ANGEL_ALREADY_DELETED = {"code": 409, "detail": "GREEN_ANGEL_ALREADY_DELETED", "description": "The green angel is already deleted"}
    USER_EXIST = {"code": 409, "detail": "USER_EXIST", "description": "The user already exists"}
    UNAUTHORIZED = {"code": 401, "detail": "UNAUTHORIZED", "description": "Invalid credentials"}
    BAD_FORMAT_PASSWORD = {"code": 400, "detail": "BAD_FORMAT_PASSWORD", "description": "The password format is invalid"}

    def __init__(self, details):
        self.code = details["code"]
        self.message = details["detail"]
        self.description = details["description"]
