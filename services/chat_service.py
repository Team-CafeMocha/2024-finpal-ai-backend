from typing import Optional

from ai_models.langchain_model import LangchainModel
from models.chat import Chat
from models.query import Query


class ChatService:
    langchain_model = LangchainModel()

    def query(self, chat_id: Optional[int], query: str) -> Query:
        result = self.langchain_model.query(query=query, chat_history=[])
        query = Query(chat_id=chat_id,
                      id=0,
                      query=result["question"],
                      answer=result["answer"],
                      model=self.langchain_model.repo_id)
        return query

    def load_chat_history(self, chat_id) -> Chat:
        return
