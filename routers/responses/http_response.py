from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')


class HttpResponse(BaseModel, Generic[T]):
    isSuccess: bool
    data: Optional[T]
    error_message: Optional[str]

    def __init__(self, data: Optional[T] = None, error: Optional[Exception] = None):
        super().__init__()
        self.isSuccess = error is None
        self.data = data if error is None else None
        self.error = f"{error}"

    class Config:
        arbitrary_types_allowed = True
