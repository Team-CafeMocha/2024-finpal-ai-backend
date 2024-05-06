from pydantic import BaseModel
from typing import Optional
import datetime


class Query(BaseModel):
    chat_id: Optional[int]
    id: int
    query: str
    answer: str
    model: str
    created_at: datetime.datetime

    def __init__(self, chat_id: Optional[int], id: int, query: str, answer: str, model: str):
        super().__init__()
        self.chat_id = chat_id
        self.id = id
        self.query = query
        self.answer = answer
        self.model = model

    class Config:
        arbitrary_types_allowed = True
        