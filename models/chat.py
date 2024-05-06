from typing import List, Optional
from pydantic import BaseModel, SkipValidation, ConfigDict
from models.query import Query
from datetime import datetime


class ChatBase(BaseModel):
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    queries: List[SkipValidation[Query]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def __init__(self, id: int,
                 description: str,
                 queries: [Query],
                 created_at: datetime):
        super().__init__()
        self.id = id
        self.description = description
        self.queries = queries
        self.created_at = created_at
