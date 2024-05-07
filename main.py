from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

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


for controller in [embed_controller, chat_controller, user_controller]:
    app.include_router(controller.router)
