from fastapi import FastAPI, Form, UploadFile

from Requests import (ChatRequest)
from Responses import (ChatResponse, EmbedResponse)
from Model.MockUpModel import MockUpModel


app = FastAPI()
model = MockUpModel()


@app.get("/")
async def root():
    return {"title": "FinPal", "description": "Chat with FinPal AI", "model": model.identifier}


@app.post("/chat/")
async def chat(chatRequest: ChatRequest):
    requestContent = chatRequest.content
    responseContent = await model.chat_response(requestContent)
    return ChatResponse(requestContent, responseContent).toResponse()

@app.post("/embed/")
async def embed(file: UploadFile):
    response = await model.embed_response(file)
    return EmbedResponse(file.filename, response).toResponse()