from fastapi import HTTPException, status

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictError(HTTPException):
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class RateLimitError(HTTPException):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail) 