from fastapi import FastAPI

# environment settings
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from controllers import (chat_controller,
                         embed_controller,
                         user_controller)

app = FastAPI()

for controller in [chat_controller, embed_controller, user_controller]:
    app.include_router(controller.router)
