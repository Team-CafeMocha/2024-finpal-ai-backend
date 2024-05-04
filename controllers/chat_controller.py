from fastapi import APIRouter

router = APIRouter(
	prefix="/chat",
    tags=["chat"]
)

@router.get("/")
async def root():
    return {"message": "CHAT API"}

@router.get("/")
async def create_chat():
    return {"message": "CHAT API"}
