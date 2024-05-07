from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')


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
            self.error = f"{type(error)}"
            self.error_message = f"{error}"
            print(type(error), error)

    class Config:
        arbitrary_types_allowed = True