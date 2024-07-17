from datetime import time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class SignUpRequest(BaseModel):
    id: str
    name: str
    password: str
    balance: int


class SignInRequest(BaseModel):
    id: str
    password: str


class DailyResponse(BaseModel):
    id: int
    balance: int
    profit: int
    day: int


class MonthlyResponse(BaseModel):
    payments: List[DailyResponse]


class PaymentResponse(BaseModel):
    id: int
    title: str
    value: int
    description: Optional[str]
    time: time
    tag: Optional[str]


class DailyPaymentsResponse(BaseModel):
    balance: int
    profit: int
    payments: List[PaymentResponse]


class StatisticsPaymentsResponse(BaseModel):
    statistics: dict


class PaymentType(str, Enum):
    income = 1
    expenditure = 2


class WritePaymentRequest(BaseModel):
    title: str
    value: int
    description: Optional[str]
    time: time
    tag: Optional[str]
    typ: PaymentType


class CommentResponse(BaseModel):
    name: str
    nickname: str
    description: Optional[str]