from fastapi import APIRouter
from services.chat_service import ChatService
from controllers.requests.chat_request import QueryRequest

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

service = ChatService()


@router.get("/")
async def root():
    return {"message": "CHAT API"}


@router.post("/query/")
async def create_query(queryRequest: QueryRequest):
    """
    쿼리 요청 \n
    :param queryRequest: 쿼리 요청 \n
    :return: 채팅 기록 전체 \n
    """
    return service.query(chat_id=queryRequest.chat_id, query=queryRequest.content)


@router.delete("/query/{query_id}")
async def delete_query(query_id: int):
    """
    쿼리 삭제 (미완료) \n
    :param query_id: 쿼리 ID \n
    :return: 삭제된 쿼리 \n
    """
    return


@router.get("/{chat_id}/")
async def read_chat_history(chat_id: int):
    """
    채팅 기록 로드 (미완료) \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    return {"chat_id": chat_id}


@router.delete("/{chat_id}/")
async def delete_chat_history(chat_id: int):
    """
    채팅 기록 삭제 (미완료) \n
    :param chat_id: 채팅 ID \n
    :return: 채팅 기록 \n
    """
    return {"chat_id": chat_id}
