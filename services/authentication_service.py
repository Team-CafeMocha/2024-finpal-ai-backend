import os
from typing import Optional
import requests

from models.token import Token
from firebase_admin import auth

from models.user import User
from services.exceptions.account_exception import AccountException


class AuthenticationService:
    __API_KEY = os.environ["FIREBASE_API_KEY"]
    __AUTHENTICATION_URL = os.environ["FIREBASE_AUTHENTICATION_URL"]
    __url = f"{__AUTHENTICATION_URL}?key={__API_KEY}"

    def sign_up(self, email: str, password: str) -> User:
        user = auth.create_user(
            email=email,
            password=password
        )
        return User(uid=user.uid)

    def sign_in(self, email: str, password: str) -> Optional[Token]:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(self.__url, json=data, headers=headers)
        result = response.json()
        if not (200 <= response.status_code < 300): raise AccountException(message=result['error']['message'])
        return Token(token=result['idToken'])

    def check_token_validation(self, token: Token):
        decoded_token = auth.verify_id_token(token.token)
        return decoded_token['uid']