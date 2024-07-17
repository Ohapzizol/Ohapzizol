from datetime import date, datetime, timedelta, time
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import update

from .base_class import Base
from .models.daily import Daily
from .models.pay import Pay
from .models.user import User
from .session import SessionLocal


async def exist_user_by_ids(_id: str) -> bool:
    db = SessionLocal()

    if db.query(User).filter_by(id=_id).first() is None:
        return False
    return True


async def update_user(_id: str, _name: str, _password: str, _balance: int) -> None:
    db = SessionLocal()
    try:
        db.execute(
            update(User)
            .where(User.id == _id)
            .values(
                name=_name,
                password=_password,
                balance=_balance
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def save_user(_id: str, _name: str, _password: str, _balance: int) -> None:
    if await exist_user_by_ids(_id=_id):
        raise HTTPException(status_code=409, detail="Already Exist Id")

    db = SessionLocal()
    user = User(id=_id, name=_name, password=_password, balance=_balance)
    db.add(user)
    db.commit()
    db.refresh(user)


async def save_new_payment(_title: str, _value: int, _description: Optional[str], _date: date, _time: time, _tag: str,
                           _user_id: str) -> None:
    db = SessionLocal()
    payment = Pay(id=None, title=_title, value=_value, description=_description, date=_date, time=_time, tag=_tag,
                  user_id=_user_id)
    db.add(payment)
    db.commit()
    db.refresh(payment)


async def save_daily(_profit: int, _balance: int, _user_id: str) -> None:
    db = SessionLocal()
    timestamp = date.today()
    daily = Daily(id=None, profit=_profit, balance=_balance, user_id=_user_id, year=timestamp.year,
                  month=timestamp.month, day=timestamp.day)
    db.add(daily)
    db.commit()
    db.refresh(daily)


async def update_daily(_id: int, _profit: int, _balance: int, _user_id: str) -> None:
    db = SessionLocal()
    timestamp = date.today()
    try:
        db.execute(
            update(Daily)
            .where(Daily.id == _id)
            .values(
                profit=_profit,
                balance=_balance,
                user_id=_user_id,
                year=timestamp.year,
                month=timestamp.month,
                day=timestamp.day
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def find_user_by_id(_id: str) -> User or None:
    db = SessionLocal()
    return db.query(User).filter_by(id=_id).first()


async def find_all_user() -> List[User] or None:
    db = SessionLocal()
    return db.query(User).filter_by().all()


async def find_pay_by_id(_id: int) -> Pay or None:
    db = SessionLocal()
    return db.query(Pay).filter_by(id=_id).first()


async def delete_pay_by_id(_id: int) -> None:
    db = SessionLocal()
    try:
        db.query(Pay).filter_by(id=_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


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


async def find_all_monthly_payment_by_user_id_at_now(_userId: str) -> List[Pay] or None:
    db = SessionLocal()
    timestamp = datetime.now().date()
    scop = timestamp - timedelta(days=timestamp.day)

    result = db.query(Pay).filter(Pay.user_id == _userId, scop < Pay.date).all()

    if not result:
        return None
    return result


async def find_all_payments_by_user_id_and_last_six(_userId: str) -> List[Pay] or None:
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


async def find_daily_by_user_id_and_date(_userId: str, _date: date) -> Daily or None:
    db = SessionLocal()
    result = db.query(Daily).filter(
        Daily.user_id == _userId,
        Daily.year == _date.year,
        Daily.month == _date.month,
        Daily.day == _date.day
    ).first()

    if not result:
        return None
    return result
