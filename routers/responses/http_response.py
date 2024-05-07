from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

status_code_dict = {"ValidationError": 404,
                    "RequestValidationError": 422}


class HttpResponse(BaseModel, Generic[T]):
    isSuccess: bool = True
    data: Optional[T] = None
    error: Optional[str] = None
    error_message: Optional[str] = None

    def __init__(self, data: Optional[T] = None, error: Optional[Exception] = None):
        super().__init__()
        self.isSuccess = error is None
        self.data = data if error is None else None
        if error is not None:
            self.error = f"{type(error).__name__}"
            self.error_message = f"{error}"

    def status_code(self):
        return status_code_dict[self.error]

    class Config:
        arbitrary_types_allowed = True
