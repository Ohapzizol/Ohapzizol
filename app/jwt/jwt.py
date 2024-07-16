from app.core.config import get_setting
import jwt
from datetime import datetime, timedelta

settings = get_setting()

ALGORITHM = "HS256"


def create_access_token(_sub: str):
    expire = datetime.now() + timedelta(seconds=settings.JWT_EXP)
    encoded_jwt = jwt.encode({
        'sub': _sub,
        'exp': expire,
    }, settings.JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt
