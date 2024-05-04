from fastapi import FastAPI
from controllers import (chat_controller,
                         embed_controller,
                         user_controller)

import os
from dotenv import load_dotenv

# environment settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))



app = FastAPI()

for controller in [chat_controller, embed_controller, user_controller]:
    app.include_router(controller.router)
