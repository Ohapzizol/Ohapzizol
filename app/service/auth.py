from app.dto import SignUpRequest, SignInRequest

from ..db.base import create_user, match_user_and_password, exist_tech_by_ids
from ..jwt.jwt import create_access_token
import bcrypt


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
    async def finduser(request: SignInRequest):
        return await exist_tech_by_ids(request.id)
    
    @staticmethod
    async def pwmatch(request: SignInRequest):
        pwmatch = match_user_and_password(
            request.id,
            request.password.encode("utf-8")
        )
        return pwmatch

    @staticmethod
    async def signin(request: SignInRequest):
        return create_access_token(
            { "sub": request.id }
        )
