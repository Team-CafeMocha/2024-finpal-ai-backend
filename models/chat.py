from typing import List
from pydantic import BaseModel, SkipValidation
from models.query import Query
import datetime

class Chat(BaseModel):
    id: int
    queries: List[SkipValidation[Query]]
    created_at: datetime.datetime

    def __init__(self, id: int, queries: [Query]):
        super().__init__()
        self.id = id
        self.queries = queries

    class Config:
        arbitrary_types_allowed = True
