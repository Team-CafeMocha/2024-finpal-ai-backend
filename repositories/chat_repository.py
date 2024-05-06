from entities import ChatEntity
from models.chat import Chat
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db


class ChatRepository:
    db: Session = Depends(get_db)

    def create_chat(self) -> Chat:
        db_chat = ChatEntity(description="")
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return Chat.model_validate(db_chat)

    def read_chat(self, chat_id: int) -> Chat:
        db_chat = self.db.query(ChatEntity.__tablename__).filter_by(id=chat_id).first()
        chat = Chat.model_validate(db_chat)
        return chat

    def update_chat(self, chat: Chat) -> Chat:
        db_chat = self.db.query(ChatEntity.__tablename__).filter_by(id=chat.id)
        db_chat.update(chat.model_dump())
        self.db.commit()
        self.db.refresh(db_chat)
        return Chat.model_validate(db_chat)

    def delete_chat(self, chat_id: int) -> Chat:
        db_chat = self.db.query(ChatEntity.__tablename__).filter_by(id=chat_id)
        chat = Chat.model_validate(db_chat)
        db_chat.delete()
        self.db.commit()
        return chat
