import bcrypt
from fastapi import HTTPException

from app.dto import SignUpRequest, SignInRequest
from ..db.base import create_user, find_user_by_id
from ..jwt.jwt import create_access_token


class AuthService:

    @staticmethod
    async def signup(request: SignUpRequest):
        await create_user(
            request.id,
            request.name,
            bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()),
            request.balance
        )

    @staticmethod
    async def login(request: SignInRequest):
        user = await find_user_by_id(request.id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return await create_access_token(user.id)
