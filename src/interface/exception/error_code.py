from enum import Enum


class ErrorCode(Enum):
    UNAUTHORIZED = {"code": 401, "detail": "UNAUTHORIZED", "description": "The user is not authorized."}
    EXPIRED_TOKEN = {"code": 401, "detail": "EXPIRED_TOKEN", "description": "The token has expired."}
    INVALID_TOKEN = {"code": 401, "detail": "INVALID_TOKEN", "description": "The token is invalid."}

    def __init__(self, details):
        self.code = details["code"]
        self.message = details["detail"]
        self.description = details["detail"]
