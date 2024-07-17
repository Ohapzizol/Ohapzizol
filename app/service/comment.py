from fastapi import HTTPException

from app.db.models.comment import Comment
from app.db.base import find_all_daily_by_user_id_and_year_and_month
from app.jwt.jwt import getCurrentUser
from app.dto import CommentResponse


class CommentService:

    @staticmethod
    async def createComment(_year: int, _month: int, _token: str):
        user = await getCurrentUser(_token)

        content = ''
        return CommentResponse(
            name=user.name,
            nickname=user.id,
            description=content
        )
