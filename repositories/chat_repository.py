from typing import Optional

from entities import ChatEntity
from models.chat import Chat
from sqlalchemy.orm import Session
from database import SessionLocal


class ChatRepository:
    db: Session = SessionLocal()

    def create_chat(self) -> Chat:
        db_chat = ChatEntity(description="")
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return Chat.model_validate(db_chat)

    def read_chat(self, chat_id: int) -> Optional[Chat]:
        db_chat = self.db.query(ChatEntity).filter_by(id=chat_id).first()
        if db_chat is None: return None
        chat = Chat.model_validate(db_chat)
        return chat

    def update_chat(self, chat: Chat) -> Optional[Chat]:
        db_chat_query = self.db.query(ChatEntity).filter_by(id=chat.id)
        if db_chat_query is None: return None
        db_chat = db_chat_query.first()
        db_chat_query.update(chat.model_dump())
        self.db.commit()
        self.db.refresh(db_chat)
        return Chat.model_validate(db_chat)

    def delete_chat(self, chat_id: int) -> Optional[Chat]:
        db_chat_query = self.db.query(ChatEntity).filter_by(id=chat_id)
        if db_chat_query is None: return None
        chat = Chat.model_validate(db_chat_query.first())
        db_chat_query.delete()
        self.db.commit()
        return chat

    def read_all_chat(self) -> [Chat]:
        db_chat_list = self.db.query(ChatEntity).all()
        return list(map(Chat.model_validate, db_chat_list))

