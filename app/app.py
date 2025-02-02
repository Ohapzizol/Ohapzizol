import logging
import re
from datetime import date
from http import HTTPStatus

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, Response, Header
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base, find_all_user
from app.db.session import db_engine
from app.dto import SignUpRequest, SignInRequest, MonthlyResponse, DailyPaymentsResponse, StatisticsPaymentsResponse, \
    WritePaymentRequest, CommentResponse, PredictResponse
from app.jwt.jwt import getCurrentUser
from app.service.auth import AuthService
from app.service.comment import CommentService
from app.service.daily import DailyService
from app.service.pay import PayService
from app.service.predict import PredictService


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


logging.basicConfig(level='INFO')

app = get_application()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

scheduler = AsyncIOScheduler(daemon=True, timezone='Asia/Seoul')

login_rgx = r'^[a-z]{4,}[0-9]{4,}$|^[a-z]{4,}[0-9]{4,}[a-z0-9]{0,3}$'
password_rgx = r'^[a-z]{4,}[0-9]{4,}[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]$|^[a-z]{4,}[0-9]{4,}[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?][a-z0-9]{0,2}$'

authService = AuthService()
dailyService = DailyService()
payService = PayService()
predictService = PredictService()


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
async def getMonthlyDaily(year: int = None, month: int = None,
                          authorization: str = Header(None, convert_underscores=False)) -> MonthlyResponse:
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
async def getPayments(date: date,
                      authorization: str = Header(None, convert_underscores=False)) -> DailyPaymentsResponse:
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


@app.post("/payment", status_code=HTTPStatus.CREATED)
async def writePayment(request: WritePaymentRequest,
                       authorization: str = Header(None, convert_underscores=False)) -> None:
    if 30 < len(request.title):
        raise HTTPException(400, 'title은 30자 이하입니다')
    if request.value < 0:
        raise HTTPException(400, 'value must not be negative')
    if request.description is not None and 500 < len(request.description):
        raise HTTPException(400, 'description은 500자 이하입니다')
    if request.tag is not None and 10 < len(request.tag):
        raise HTTPException(400, 'tag은 10자 이하입니다')

    await payService.createPayment(request, authorization)


@app.get("/statistics/latest", status_code=200, response_model=StatisticsPaymentsResponse)
async def getPaymentsStatistics(
        authorization: str = Header(None, convert_underscores=False)) -> StatisticsPaymentsResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await payService.getPaymentsLatestStatistics(authorization)


@app.get("/statistics/tag", status_code=200, response_model=StatisticsPaymentsResponse)
async def getPaymentsStatistics(
        authorization: str = Header(None, convert_underscores=False)) -> StatisticsPaymentsResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await payService.getPaymentsTagStatistics(authorization)


@app.get("/comment", status_code=200, response_model=CommentResponse)
async def getTodayBalanceComment(authorization: str = Header(None, convert_underscores=False)) \
        -> CommentResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return await CommentService.getBalanceComment(authorization)


@app.get("/comment/predict", status_code=200, response_model=PredictResponse)
async def getPredictComment(authorization: str = Header(None, convert_underscores=False)) -> PredictResponse:
    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    return PredictResponse(predict=await PredictService.getPredictComment(await getCurrentUser(authorization)))


async def re_training():
    users = await find_all_user()

    for user in users:
        await predictService.getPredictComment(user)


scheduler.add_job(re_training, 'cron', year='*', month='*', day='1', hour='0', minute='0')


@app.delete("/payments/{pay_id}", status_code=200)
async def delete_pay(pay_id: int, authorization: str = Header(None)):
    if pay_id is None:
        raise HTTPException(status_code=400, detail="pay_id must not be null")

    if authorization is None:
        raise HTTPException(401, "authorization must not be null")

    await payService.deleteById(_pay_id=pay_id, _token=authorization)
