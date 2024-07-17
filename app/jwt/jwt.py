from fastapi import HTTPException
from jwt import ExpiredSignatureError

from app.core.config import get_setting
import jwt
from datetime import datetime, timedelta

from app.db.models.user import User
from ..db.base import find_user_by_id

settings = get_setting()

ALGORITHM = "HS256"


async def create_access_token(_sub: str):
    expire = datetime.now() + timedelta(seconds=1)
    encoded_jwt = jwt.encode({
        'sub': _sub,
        'exp': expire,
    }, settings.JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def getCurrentUser(_token: str) -> User:

    try:
        subject = jwt.decode(_token[7::], settings.JWT_KEY, algorithms=[ALGORITHM])['sub']
        user = await find_user_by_id(subject)

        if user is None:
            raise HTTPException(401, "wrong token")

        return user
    except Exception as e:
        if isinstance(e, ExpiredSignatureError):
            raise HTTPException(403, "token has expired")
        else:
            raise e
