from sqlalchemy.exc import NoResultFound

from .base_class import Base
from .models.user import User
from .session import SessionLocal


def exist_tech_by_ids(_id: str):
    db = SessionLocal()

    try:
        db.query(User).filter_by(id=_id).first()
    except NoResultFound:
        return False
    return True


def create_user(_id: str, _name: str, _password: str, _balance: int):
    if not exist_tech_by_ids(_id=_id):
        return

    db = SessionLocal()
    user = User(id=_id, name=_name, password=_password, balance=_balance)
    db.add(user)
    db.commit()
    db.refresh(user)
