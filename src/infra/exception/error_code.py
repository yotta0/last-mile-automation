from enum import Enum


class ErrorCode(Enum):
    INVALID_TOKEN = {"code": 401, "detail": "INVALID_TOKEN", "description": "INVALID_TOKEN"}

    def __init__(self, details):
        self.code = details["code"]
        self.message = details["detail"]
        self.description = details["detail"]
