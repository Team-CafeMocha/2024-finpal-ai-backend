from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from firebase_admin import credentials
import firebase_admin
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# environment settings
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from models.root import Root
from routers.responses.http_response import HttpResponse

from routers import (
    embed_controller,
    chat_controller,
    user_controller
)

app = FastAPI()

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-adminsdk-key.json")
    default_app = firebase_admin.initialize_app(cred)


@app.get("/", response_model=Root)
def root() -> Root:
    return Root("finpal")


@app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception):
    response = HttpResponse(error=e)
    return JSONResponse(
        status_code=response.status_code(),
        content=response.model_dump()
    )


origins = ["http://localhost",
           "http://localhost:3000",
           "https://finpal.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for controller in [embed_controller, chat_controller, user_controller]:
    app.include_router(controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app")
