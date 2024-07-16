from fastapi import HTTPException

from .base_class import Base
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


async def find_by_id(_id: str) -> User or None:
    db = SessionLocal()
    return db.query(User).filter_by(id=_id).first()
