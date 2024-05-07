from fastapi import FastAPI


# environment settings
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from models.root import Root


from routers import (
    embed_controller,
    chat_controller,
    user_controller
)

app = FastAPI()


@app.get("/", response_model=Root)
def root() -> Root:
    return Root("finpal")


for controller in [embed_controller, chat_controller, user_controller]:
    app.include_router(controller.router)
