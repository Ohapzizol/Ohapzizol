import token

from fastapi import HTTPException

from app.core.config import get_setting
import jwt
from datetime import datetime, timedelta

from app.db.models.user import User
from ..db.base import find_by_id

settings = get_setting()

ALGORITHM = "HS256"


async def create_access_token(_sub: str):
    expire = datetime.now() + timedelta(seconds=settings.JWT_EXP)
    encoded_jwt = jwt.encode({
        'sub': _sub,
        'exp': expire,
    }, settings.JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def getCurrentUser(_token: str) -> User:
    subject = jwt.decode(token, settings.JWT_KEY, algorithms=[ALGORITHM]).get('sub')
    user = find_by_id(subject)

    if user is None:
        raise HTTPException(401, "wrong token")

    return user
