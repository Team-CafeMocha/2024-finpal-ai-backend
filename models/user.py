from pydantic import BaseModel


class User(BaseModel):
    uid: str = ""

    def __init__(self, uid: str):
        super().__init__()
        self.uid = uid
