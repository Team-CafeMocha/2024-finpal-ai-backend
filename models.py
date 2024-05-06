import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    queries = relationship("Query", back_populates="chat")


class Query(Base):
    __tablename__ = "query"

    chat_id = Column(Integer, ForeignKey("chat.id"))
    id: str = Column(Integer, primary_key=True, index=True)
    query: str = Column(String, index=True)
    answer: str = Column(String, index=True)
    model: str = Column(String, index=True)
    created_at: datetime.datetime = Column(DateTime, nullable=False)

    chat = relationship("Chat", back_populates="queries")


