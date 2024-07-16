from app.core.config import get_setting
from jose import jwt
from datetime import datetime, timedelta

settings = get_setting()

SECRET_KEY = settings.JWT_KEY
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=settings.JWT_EXP)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
