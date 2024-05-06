from pydantic import BaseModel
import datetime

class EmbedCount(BaseModel):
    count: int
    created_at: datetime.datetime

    def __init__(self, count: int):
        super().__init__()
        self.count = count

    class Config:
        arbitrary_types_allowed = True