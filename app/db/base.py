from datetime import date, datetime, timedelta
from typing import List

from fastapi import HTTPException

from .base_class import Base
from .models.daily import Daily
from .models.pay import Pay
from .models.user import User
from .session import SessionLocal


async def exist_tech_by_ids(_id: str) -> bool:
    db = SessionLocal()

    if db.query(User).filter_by(id=_id).first() is None:
        return False
    return True


async def create_user(_id: str, _name: str, _password: str, _balance: int) -> None:
    if await exist_tech_by_ids(_id=_id):
        raise HTTPException(status_code=409, detail="Already Exist Id")

    db = SessionLocal()
    user = User(id=_id, name=_name, password=_password, balance=_balance)
    db.add(user)
    db.commit()
    db.refresh(user)


async def find_user_by_id(_id: str) -> User or None:
    db = SessionLocal()
    return db.query(User).filter_by(id=_id).first()


async def find_all_daily_by_user_id_and_year_and_month(_userId: str, _year: int, _month: int) -> List[Daily] or None:
    db = SessionLocal()
    result = db.query(Daily).order_by(Daily.day.asc()).filter(Daily.user_id == _userId, Daily.year == _year,
                                                              Daily.month == _month).all()

    if not result:
        return None
    return result


async def find_all_payments_by_user_id_and_date(_userId: str, _date: date) -> List[Pay] or None:
    db = SessionLocal()
    result = db.query(Pay).order_by(Pay.time.desc()).filter(Pay.user_id == _userId, Pay.date == _date).all()
    if not result:
        return None
    return result


async def find_all_payments_by_user_id_last_six(_userId: str) -> List[Pay] or None:
    db = SessionLocal()
    timestamp = datetime.now().date()
    scop = timestamp - timedelta(weeks=5)

    result = db.query(Pay).order_by(Pay.date.desc(), Pay.time.desc()).filter(
        Pay.user_id == _userId,
        scop <= Pay.date,
        Pay.date <= timestamp
    ).all()
    if not result:
        return None
    return result


async def find_daily_by_user_id_at_now(_userId: str) -> Daily or None:
    db = SessionLocal()

    timestamp = datetime.now()
    result = db.query(Daily).filter(
        Daily.user_id == _userId,
        Daily.year == timestamp.year,
        Daily.month == timestamp.month,
        Daily.day == timestamp.day
    ).first()

    if not result:
        return None
    return result
