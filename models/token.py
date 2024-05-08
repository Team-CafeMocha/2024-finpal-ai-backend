from pydantic import BaseModel

class Token(BaseModel):
    token: str = ""

    def __init__(self, token):
        super().__init__()
        self.token = token