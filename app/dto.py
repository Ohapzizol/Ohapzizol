from pydantic import BaseModel


class SignUpRequest(BaseModel):
    id: str
    name: str
    password: str
    balance: int
