from pydantic import BaseModel
import datetime


class Root(BaseModel):
    name: str = ""
    status: str = ""

    def __init__(self, name: str, status="activate"):
        super().__init__()
        self.name = name
        self.status = status

    class Config:
        arbitrary_types_allowed = True
