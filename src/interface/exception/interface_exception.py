from src.interface.exception.error_code import ErrorCode


class InterfaceException(Exception):
    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
