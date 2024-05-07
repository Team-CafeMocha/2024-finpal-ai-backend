from fastapi import (APIRouter, UploadFile, status)

from models.embed_result import EmbedResult
from models.embed_count import EmbedCount
from models.root import Root
from routers.responses.http_response import HttpResponse
from services.embed_service import EmbedService

router = APIRouter(
    prefix="/embed",
    tags=["embed"]
)

service = EmbedService()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=Root)
async def root() -> Root:
    return Root("Embed API")


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=HttpResponse[EmbedResult])
async def create_embed(file: UploadFile) -> HttpResponse[EmbedResult]:
    """
    임베딩 \n
    :param file: 임베딩 할 파일(pdf - 수정 필요, 사용 가능) \n
    :return: 임베딩 된 파일 이름 \n
    """
    embed_result = service.embed(file)
    return HttpResponse(embed_result)


@router.get("/count",
            status_code=status.HTTP_200_OK,
            response_model=HttpResponse[EmbedCount])
async def read_embed_data_count() -> HttpResponse[EmbedCount]:
    """
    임베딩 데이터 개수 \n
    :return: 임베딩 된 데이터 개수 반환 \n
    """
    embed_count = service.count()
    return HttpResponse(embed_count)
