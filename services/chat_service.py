from ai_models.langchain_model import LangchainModel

class ChatService:
    langchain_model = LangchainModel()

    def query(self, chat_id: int, query: str):
        return self.langchain_model.query(query=query, chat_history=[])

    def load_chat_history(self, chat_id):
        return