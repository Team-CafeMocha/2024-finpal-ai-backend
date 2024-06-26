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

responses = {
    404: {'model': HttpResponse, 'description': 'Not Found Error'},
    422: {'model': HttpResponse, 'description': 'Validation Error'}
}


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=Root)
async def root() -> Root:
    return Root("Chat API")


@router.post("/query/",
             status_code=status.HTTP_201_CREATED,
             response_model=HttpResponse[Query],
             responses={**responses})
async def create_query(query_request: QueryRequest) -> HttpResponse[Query]:
    """
    쿼리 요청 \n
    :param query_request: 쿼리 요청 \n
    :return: 생성된 쿼리 (질문, 답변) \n
    """
    query = service.query(chat_id=query_request.chat_id, query=query_request.query)
    return HttpResponse[Query](query)


@router.delete("/query/{query_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={**responses})
async def delete_query(query_id: int):
    """
    쿼리 삭제 \n
    :param query_id: 쿼리 ID \n
    :return: 삭제된 쿼리 \n
    """
    query = service.remove_query(query_id=query_id)


@router.get("/list/",
            status_code=status.HTTP_200_OK,
            response_model=HttpResponse[List[Chat]],
            responses={**responses})
async def read_chat_list() -> HttpResponse[List[Chat]]:
    """
    모든 채팅 기록 불러오기 \n
    :return: 모든 채팅 기록 \n
    """
    chat_list = service.read_all_chat()
    return HttpResponse[List[Chat]](chat_list)


@router.get("/{chat_id}/",
            status_code=status.HTTP_200_OK,
            response_model=HttpResponse[Chat],
            responses={**responses})
async def read_chat(chat_id: int) -> HttpResponse[Chat]:
    """
    채팅 기록 불러오기 \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    chat = service.load_chat(chat_id=chat_id)
    return HttpResponse[Chat](chat)


@router.delete("/{chat_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={**responses})
async def delete_chat(chat_id: int):
    """
    채팅 기록 삭제 \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    chat = service.remove_chat(chat_id=chat_id)
