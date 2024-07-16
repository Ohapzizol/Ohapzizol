import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException

from app.db.session import db_engine
from app.db.base import Base
import re

from app.dto import SignUpRequest
from app.service.auth import AuthService


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


def validate_string(_input_str: str, _pattern: str):
    pattern = _pattern
    if re.match(pattern, _input_str):
        return True
    else:
        return False


@app.post("/signup")
async def signup(request: SignUpRequest) -> None:
    if 4 < len(request.name):
        raise HTTPException(status_code=400, detail="이름은 4자리 이상일 수 없습니다.")
    if not validate_string(request.id, login_rgx):
        raise HTTPException(status_code=400, detail="아이디는 영문 소문자 4자리 이상, 숫자 4자리 이상, 최대 15자리 이하의 문자열입니다.")
    if not validate_string(request.password, password_rgx):
        raise HTTPException(status_code=400, detail="비밀번호는 영문 소문자 4자리 이상, 숫자 4자리 이상, 특수문자 한자리 이상, 최대 15자리 이하의 문자열입니다.")

    await authService.signup(request)
