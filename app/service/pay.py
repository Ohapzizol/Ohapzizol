from datetime import date
from typing import List

from fastapi import HTTPException

from app.db.base import find_all_payments_by_user_id_and_date, find_all_payments_by_user_id_last_six
from app.db.models.pay import Pay
from app.db.models.user import User
from app.dto import PaymentResponse, StatisticsPaymentsResponse
from app.jwt.jwt import getCurrentUser


class PayService:

    @staticmethod
    async def getPaymentsByDate(_date: date, _user: User) -> List[PaymentResponse]:
        payments = await find_all_payments_by_user_id_and_date(_userId=_user.id, _date=_date)

        if not payments:
            raise HTTPException(204, "There is no payment for this date" + str(_date))

        return [PaymentResponse(
            id=pay.id,
            name=pay.name,
            value=pay.value,
            description=pay.description,
            tag=pay.tag,
            time=pay.time
        ) for pay in payments]

    @staticmethod
    async def getPaymentsLatestStatistics(_token: str) -> StatisticsPaymentsResponse:
        user = await getCurrentUser(_token)

        payments = await find_all_payments_by_user_id_last_six(user.id)

        if not payments:
            raise HTTPException(204, "There is no payment")

        response = {i: {'expenditure': 0, 'income': 0} for i in range(6)}
        now = date.today()

        for pay in payments:
            key = int((now - pay.date).days / 7)

            if pay.value < 0:
                response[key]['expenditure'] -= pay.value
            else:
                response[key]['income'] += pay.value

        return StatisticsPaymentsResponse(statistics=response)

