from fastapi import APIRouter

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


@router.get("/")
async def root() -> Root:
    return Root("Chat API")


@router.post("/query/")
async def create_query(queryRequest: QueryRequest) -> HttpResponse[Query]:
    """
    쿼리 요청 \n
    :param queryRequest: 쿼리 요청 \n
    :return: 생성된 쿼리 (질문, 답변) \n
    """
    try:
        query = service.query(chat_id=queryRequest.chat_id, query=queryRequest.query)
        return HttpResponse[Query](query)
    except Exception as e:
        return HttpResponse[Query](error=e)


@router.delete("/query/{query_id}")
async def delete_query(query_id: int) -> HttpResponse[Query]:
    """
    쿼리 삭제 (미구현) \n
    :param query_id: 쿼리 ID \n
    :return: 삭제된 쿼리 \n
    """
    try:
        query = Query(chat_id=0, id=10, query="str", answer="str", model="str")
        return HttpResponse[Query](query)
    except Exception as e:
        return HttpResponse[Query](error=e)


@router.get("/{chat_id}/")
async def read_chat_history(chat_id: int) -> HttpResponse[Chat]:
    """
    채팅 기록 로드 (미구현) \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    try:
        chat = Chat(id=0, queries=[])
        return HttpResponse(chat)
    except Exception as e:
        return HttpResponse[Chat](error=e)


@router.delete("/{chat_id}/")
async def delete_chat_history(chat_id: int) -> HttpResponse[Chat]:
    """
    채팅 기록 삭제 (미구현) \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    try:
        chat = Chat(id=0, queries=[])
        return HttpResponse(chat)
    except Exception as e:
        return HttpResponse[Chat](error=e)
