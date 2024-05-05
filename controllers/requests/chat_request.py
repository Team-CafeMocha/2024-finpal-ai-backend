from pydantic import BaseModel

class QueryRequest(BaseModel):
    chat_id: (int | None)
    content: str