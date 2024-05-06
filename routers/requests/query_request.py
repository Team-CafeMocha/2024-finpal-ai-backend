from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    chat_id: Optional[int] = None
    query: str