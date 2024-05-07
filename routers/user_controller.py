from fastapi import APIRouter
from firebase_admin import auth
from models.account import SignUpSchema, LoginSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import requests
from models.root import Root
import os

router = APIRouter(
	prefix="/user",
    tags=["user"]
)

@router.get("/")
async def root() -> Root:
    return Root("User API")

@router.post('/signup')
async def create_an_account(user_data:SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user =  auth.create_user(
            email = email,
            password = password
        )

        return JSONResponse(content={"message":f" {user.uid}의 계정이 성공적으로 생성되었습니다."},
                            status_code= 201
                )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code= 400,
            detail= f"{email}이 사용된 계정이 이미 존재합니다."
        )
    
@router.post("/login")
async def login(user_data: LoginSchema):
    API_KEY = os.environ["FIREBASE_API_KEY"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": user_data.email,
        "password": user_data.password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    if response.status_code == 200:
        return JSONResponse(content={"token": result['idToken']}, status_code=200)
    else:
        raise HTTPException(status_code=response.status_code, detail=result.get("error", {}).get("message", "An error occurred"))
    

@router.post("/ping")
async def validate_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return JSONResponse(content={"uid": decoded_token['uid']}, status_code=200)
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")