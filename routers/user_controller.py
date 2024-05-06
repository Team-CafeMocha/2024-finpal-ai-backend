from fastapi import APIRouter

from models.root import Root

router = APIRouter(
	prefix="/user",
    tags=["user"]
)

@router.get("/")
async def root() -> Root:
    return Root("User API")

