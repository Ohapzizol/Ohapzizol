from pydantic import BaseModel


class SignUpRequest(BaseModel):
    id: str
    name: str
    password: str
    balance: int

class SignInRequest(BaseModel):
    id: str
    password: str
