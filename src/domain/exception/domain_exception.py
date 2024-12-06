from src.domain.exception.error_code import ErrorCode


class DomainException(Exception):
    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
