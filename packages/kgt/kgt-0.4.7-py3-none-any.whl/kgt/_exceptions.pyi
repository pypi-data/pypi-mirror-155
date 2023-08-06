from _typeshed import Incomplete

class ValidationError(Exception):
    code: Incomplete
    timestamp: Incomplete
    def __init__(self, message, code, timestamp: Incomplete | None = ...) -> None: ...

class LicenseError(Exception): ...
