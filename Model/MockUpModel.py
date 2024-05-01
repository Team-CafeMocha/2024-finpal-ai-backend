from fastapi import UploadFile
from Model.Abstract.AbstractModel import AbstractModel
import asyncio

class MockUpModel(AbstractModel):
    identifier = "mockup"

    async def chat_response(self, content):
        await asyncio.sleep(15)
        return content

    async def embed_response(self, embed_file: UploadFile):
        return f"test: {embed_file.filename} is uploaded"
