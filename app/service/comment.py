from datetime import date

from fastapi import HTTPException

from app.db.base import find_all_monthly_payment_by_user_id_at_now
from app.dto import CommentResponse
from app.jwt.jwt import getCurrentUser


class CommentService:

    @staticmethod
    async def getBalanceComment(_token: str):
        user = await getCurrentUser(_token)

        payments = await find_all_monthly_payment_by_user_id_at_now(user.id)

        evaluation: str
        if payments is None:
            evaluation = '이번 달은 가계부를 작성하지 않았습니다.'
        else:
            balance = sum([pay.value for pay in payments])
            if 0 < balance:
                evaluation = '이번 달은 흑자입니다.'
            elif 0 == balance:
                evaluation = '이번 달은 어떤 수익도 없습니다.'
            else:
                evaluation = '이번 달은 적자입니다.'

        return CommentResponse(
            name=user.name,
            nickname=user.id,
            balance=f'현재 잔고는 {format(user.balance, ",")}원 입니다.',
            evaluation=evaluation
        )
