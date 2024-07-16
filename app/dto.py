from typing import List

from pydantic import BaseModel


class SignUpRequest(BaseModel):
    id: str
    name: str
    password: str
    balance: int


class SignInRequest(BaseModel):
    id: str
    password: str


class MonthlyPaymentResponse(BaseModel):
    id: int
    balance: int
    profit: int
    day: int


class MonthlyPaymentListResponse(BaseModel):
    payments: List[MonthlyPaymentResponse]
