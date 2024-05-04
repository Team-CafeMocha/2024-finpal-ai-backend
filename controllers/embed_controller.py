from fastapi import APIRouter
from services.embed_service import EmbedService

router = APIRouter(
	prefix="/embed",
    tags=["embed"]
)

service = EmbedService()

@router.get("/")
async def root():
    return {"message": "EMBED API"}

# @router.post("/embed/")
# async def create_embed(file: UploadFile):
#     response = await model.embed_response(file)
#     return EmbedResponse(file.filename, response).toResponse()

@router.get("/embed/count")
async def read_embed_data_count():
    return service.count()