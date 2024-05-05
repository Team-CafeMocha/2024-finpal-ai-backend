from fastapi import (APIRouter, UploadFile)
from services.embed_service import EmbedService

router = APIRouter(
	prefix="/embed",
    tags=["embed"]
)

service = EmbedService()

@router.get("/")
async def root():
    return {"message": "EMBED API"}

@router.post("/")
async def create_embed(file: UploadFile):
    """
    임베딩 \n
    :param file: 임베딩 할 파일(pdf) \n
    :return: 임베딩 된 파일 이름 \n
    """
    return service.embed(file)

@router.get("/count")
async def read_embed_data_count():
    """
    임베딩 데이터 개수 \n
    :return: 임베딩 된 데이터 개수 반환 \n
    """
    return service.count()