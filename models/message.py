from pydantic import BaseModel


class Message(BaseModel):
    message: str = ""

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    class Config:
        arbitrary_types_allowed = True