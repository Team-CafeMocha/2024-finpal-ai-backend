from typing import List

from fastapi import APIRouter, status

from models.chat import Chat
from models.query import Query
from models.root import Root
from routers.responses.http_response import HttpResponse
from services.chat_service import ChatService
from routers.requests.query_request import QueryRequest

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

service = ChatService()


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=Root)
async def root() -> Root:
    return Root("Chat API")


@router.post("/query/",
             status_code=status.HTTP_201_CREATED,
             response_model=HttpResponse[Query])
async def create_query(queryRequest: QueryRequest) -> HttpResponse[Query]:
    """
    쿼리 요청 \n
    :param queryRequest: 쿼리 요청 \n
    :return: 생성된 쿼리 (질문, 답변) \n
    """
    query = service.query(chat_id=queryRequest.chat_id, query=queryRequest.query)
    return HttpResponse[Query](query)


@router.delete("/query/{query_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_query(query_id: int):
    """
    쿼리 삭제 \n
    :param query_id: 쿼리 ID \n
    :return: 삭제된 쿼리 \n
    """
    query = service.remove_query(query_id=query_id)


@router.get("/list/",
            status_code=status.HTTP_200_OK,
            response_model=HttpResponse[List[Chat]])
async def read_chat_list() -> HttpResponse[List[Chat]]:
    """
    모든 채팅 기록 불러오기 \n
    :return: 모든 채팅 기록 \n
    """
    chat_list = service.read_all_chat()
    return HttpResponse[List[Chat]](chat_list)


@router.get("/{chat_id}/",
            status_code=status.HTTP_200_OK,
            response_model=HttpResponse[Chat])
async def read_chat(chat_id: int) -> HttpResponse[Chat]:
    """
    채팅 기록 불러오기 \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    chat = service.load_chat(chat_id=chat_id)
    return HttpResponse[Chat](chat)


@router.delete("/{chat_id}/",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int):
    """
    채팅 기록 삭제 \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    chat = service.remove_chat(chat_id=chat_id)
