from abc import *

class AbstractModel(metaclass=ABCMeta):
    identifier: str = "untitled"

    @abstractmethod
    async def chat_response(self, content):
        pass

    @abstractmethod
    async def embed_response(self, embed_file):
        pass
