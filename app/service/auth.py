from app.dto import SignUpRequest

from ..db.base import create_user
import bcrypt


class AuthService:

    @staticmethod
    async def signup(request: SignUpRequest):
        create_user(
            request.id,
            request.name,
            bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()),
            request.balance
        )
