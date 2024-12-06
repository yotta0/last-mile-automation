from src.domain.exception.error_code import ErrorCode


class InfraException(Exception):
    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
