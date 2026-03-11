from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, entity: str):
        super().__init__(status_code=404, detail=f"{entity} not found")


class AlreadyExistsException(HTTPException):
    def __init__(self, entity: str):
        super().__init__(status_code=400, detail=f"{entity} already exists")


class BusinessLogicException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)


class ValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=401, detail=message)
