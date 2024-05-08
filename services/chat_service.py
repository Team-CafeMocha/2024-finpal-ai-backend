from typing import Optional, List

from ai_models.langchain_model import LangchainModel
from repositories.chat_repository import ChatRepository
from repositories.query_repository import QueryRepository
from models.chat import (Chat)
from models.query import (Query, QueryCreate)


class ChatService:
    langchain_model = LangchainModel()
    chat_repository = ChatRepository()
    query_repository = QueryRepository()

    def query(self, chat_id: Optional[int], query: str) -> Query:
        chat_history = []
        if chat_id is None:
            chat_id = self.chat_repository.create_chat().id
        else:
            chat_history = self.chat_repository.read_chat(chat_id).history()

        result = self.langchain_model.query(query=query, chat_history=chat_history)
        query_create = QueryCreate(chat_id=chat_id,
                            query=result["question"],
                            answer=result["answer"],
                            model=self.langchain_model.repo_id)
        query_result = self.query_repository.create_query(queryCreate=query_create)
        return query_result

    def load_chat(self, chat_id: int) -> Chat:
        return self.chat_repository.read_chat(chat_id=chat_id)

    def read_all_chat(self) -> List[Chat]:
        return self.chat_repository.read_all_chat()

    def remove_query(self, query_id: int) -> Query:
        return self.query_repository.delete_query(query_id=query_id)

    def remove_chat(self, chat_id: int) -> Chat:
        return self.chat_repository.delete_chat(chat_id=chat_id)