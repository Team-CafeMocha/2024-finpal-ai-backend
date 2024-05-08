from fastapi import APIRouter, status

from models.root import Root
from models.message import Message
from models.token import Token
from models.user import User
from routers.requests.account_request import AccountRequest
from routers.requests.token_request import TokenRequest
from routers.responses.http_response import HttpResponse
from services.authentication_service import AuthenticationService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

authentication_service = AuthenticationService()


@router.get("/")
async def root() -> Root:
    return Root("User API")


@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=HttpResponse[Message])
async def create_an_account(account_request: AccountRequest) -> HttpResponse[Message]:
    user = authentication_service.sign_up(email=account_request.email, password=account_request.password)
    message = Message(message=f" {user.uid}의 계정이 성공적으로 생성되었습니다.")
    print(message.model_dump())
    return HttpResponse[Message](message)


@router.post("/login",
             status_code=status.HTTP_200_OK,
             response_model=HttpResponse[Token])
async def login(account_request: AccountRequest):
    token = authentication_service.sign_in(email=account_request.email, password=account_request.password)
    return HttpResponse[Token](token)


@router.post("/ping",
             status_code=status.HTTP_200_OK,
             response_model=HttpResponse[User])
async def validate_token(token_request: TokenRequest):
    token = Token(token=token_request.token)
    user = authentication_service.check_token_validation(token)
    return HttpResponse[User](user)
