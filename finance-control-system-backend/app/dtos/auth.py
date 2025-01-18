from pydantic import BaseModel


class UserLoginDto(BaseModel):
    username: str
    password: str

class UserRegisterDto(BaseModel):
    username: str
    telegram_id: int
    password: str

class AccessTokenDto(BaseModel):
    access_token: str
