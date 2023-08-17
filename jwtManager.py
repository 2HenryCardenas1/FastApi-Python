from fastapi import HTTPException, Request
from jwt import decode, encode


class JwtManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_token(self, payload):
        return encode(payload, self.secret_key, algorithm="HS256")

    def validate_token(self, token) -> dict:
        data: dict = decode(token, self.secret_key, algorithms="HS256")  
        return data
