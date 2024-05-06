from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class QueryBase(BaseModel):
    chat_id: Optional[int]
    query: str
    answer: str
    model: str

    class Config:
        arbitrary_types_allowed = True


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: int
    created_at: datetime

    def __init__(self, chat_id: Optional[int], id: int, query: str, answer: str, model: str):
        super().__init__()
        self.chat_id = chat_id
        self.id = id
        self.query = query
        self.answer = answer
        self.model = model

    model_config = ConfigDict(from_attributes=True)
