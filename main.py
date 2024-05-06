from fastapi import FastAPI

# environment settings
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

import entities

from routers import (
    embed_controller,
    chat_controller,
    user_controller
)

app = FastAPI()

@app.get("/")
def root() -> dict:
    return {"status": "activate"}


for controller in [embed_controller, chat_controller, user_controller]:
    app.include_router(controller.router)
