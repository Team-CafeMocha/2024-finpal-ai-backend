from pydantic import BaseModel

class ChatRequest(BaseModel):
    uid: str
    content: str