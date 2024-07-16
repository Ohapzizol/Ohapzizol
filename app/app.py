import logging
import re
from datetime import date
from http import HTTPStatus

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, Response, Header

from app.db.base import Base
from app.db.session import db_engine
from app.dto import SignUpRequest, SignInRequest, MonthlyResponse, DailyPaymentsResponse, StatisticsPaymentsResponse
from app.jwt.jwt import getCurrentUser
from app.service.auth import AuthService
from app.service.daily import DailyService
from app.service.pay import PayService


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


logging.basicConfig(level='INFO')

app = get_application()

scheduler = AsyncIOScheduler(daemon=True, timezone='Asia/Seoul')

login_rgx = r'^[a-z]{4,}[0-9]{4,}$|^[a-z]{4,}[0-9]{4,}[a-z0-9]{0,3}$'
password_rgx = r'^[a-z]{4,}[0-9]{4,}[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]$|^[a-z]{4,}[0-9]{4,}[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?][a-z0-9]{0,2}$'

authService = AuthService()
dailyService = DailyService()
payService = PayService()


def validate_string(_input_str: str, _pattern: str):
    pattern = _pattern
    if re.match(pattern, _input_str):
        return True
    else:
        return False


@app.post("/signup", status_code=HTTPStatus.CREATED)
async def signup(request: SignUpRequest) -> None:
    if 4 < len(request.name):
        raise HTTPException(status_code=400, detail="이름은 4자리 이상일 수 없습니다.")
    if not validate_string(request.id, login_rgx):
        raise HTTPException(status_code=400, detail="아이디는 영문 소문자 4자리 이상, 숫자 4자리 이상, 최대 15자리 이하의 문자열입니다.")
    if not validate_string(request.password, password_rgx):
        raise HTTPException(status_code=400, detail="비밀번호는 영문 소문자 4자리 이상, 숫자 4자리 이상, 특수문자 한자리 이상, 최대 15자리 이하의 문자열입니다.")

    await authService.signup(request)


@app.post("/login", status_code=HTTPStatus.OK)
async def login(request: SignInRequest, response: Response) -> None:
    if not validate_string(request.id, login_rgx):
        raise HTTPException(status_code=400, detail="아이디는 영문 소문자 4자리 이상, 숫자 4자리 이상, 최대 15자리 이하의 문자열입니다.")
    if not validate_string(request.password, password_rgx):
        raise HTTPException(status_code=400, detail="비밀번호는 영문 소문자 4자리 이상, 숫자 4자리 이상, 특수문자 한자리 이상, 최대 15자리 이하의 문자열입니다.")

    response.headers.append(key='Authorization', value=await authService.login(request))


@app.get("/daily/monthly", status_code=HTTPStatus.OK, response_model=MonthlyResponse)
async def getMonthlyDaily(year: int = None, month: int = None, authorization: str = Header(None, convert_underscores=False)) -> MonthlyResponse:
    if year is None:
        raise HTTPException(400, "year must not be null")

    if month is None:
        raise HTTPException(400, "month must not be null")
    elif month < 1 or month > 12:
        raise HTTPException(400, "month must be between 1 and 12")

    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await dailyService.getMonthlyDaily(year, month, authorization)


@app.get("/payments", status_code=200, response_model=DailyPaymentsResponse)
async def getPayments(date: date, authorization: str = Header(None, convert_underscores=False)) -> DailyPaymentsResponse:
    if date is None:
        raise HTTPException(400, "date must not be null")
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    user = await getCurrentUser(authorization)

    payments = await payService.getPaymentsByDate(date, user)
    profit, balance = await dailyService.getDaily(user)

    return DailyPaymentsResponse(
        profit=profit,
        balance=balance,
        payments=payments
    )


@app.get("/statistics/latest", status_code=200, response_model=StatisticsPaymentsResponse)
async def getPaymentsStatistics(authorization: str = Header(None, convert_underscores=False)) -> StatisticsPaymentsResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await payService.getPaymentsLatestStatistics(authorization)


@app.get("/statistics/tag", status_code=200, response_model=StatisticsPaymentsResponse)
async def getPaymentsStatistics(authorization: str = Header(None, convert_underscores=False)) -> StatisticsPaymentsResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await payService.getPaymentsTagStatistics(authorization)
