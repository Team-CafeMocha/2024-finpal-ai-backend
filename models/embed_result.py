from pydantic import BaseModel
import datetime


class EmbedResult(BaseModel):
    embedded_filename: str
    created_at: datetime.datetime

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    class Config:
        arbitrary_types_allowed = True
