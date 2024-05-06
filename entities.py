from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class ChatEntity(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    queries = relationship("QueryEntity", back_populates="chat")
    created_at = Column(DateTime, default=datetime.now, index=True)


class QueryEntity(Base):
    __tablename__ = "query"

    chat_id = Column(Integer, ForeignKey("chat.id"))
    id: str = Column(Integer, primary_key=True, index=True)
    query: str = Column(String, index=True)
    answer: str = Column(String, index=True)
    model: str = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)

    chat = relationship("ChatEntity", back_populates="queries")
