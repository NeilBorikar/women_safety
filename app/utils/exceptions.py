from fastapi import HTTPException


class AppException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(404, message)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(401, message)


class BadRequestException(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(400, message)