from datetime import date
from typing import List

from fastapi import HTTPException

from app.db.base import find_all_payments_by_user_id
from app.db.models.user import User
from app.dto import PaymentResponse


class PayService:

    @staticmethod
    async def getPaymentsByDate(_date: date, _user: User) -> List[PaymentResponse]:

        payments = await find_all_payments_by_user_id(_userId=_user.id, _date=_date)

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
