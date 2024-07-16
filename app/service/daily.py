from fastapi import HTTPException

from app.db.base import find_pay_by_user_id_and_year_and_month
from app.dto import MonthlyPaymentListResponse, MonthlyPaymentResponse
from app.jwt.jwt import getCurrentUser


class DailyService:

    @staticmethod
    async def getMonthlyPay(_year: int, _month: int, _token: str) -> MonthlyPaymentListResponse:
        user = await getCurrentUser(_token)

        dailies = await find_pay_by_user_id_and_year_and_month(user.id, _year, _month)

        if not dailies:
            raise HTTPException(204, "There is no content by date: " + str(_year) + '.' + str(_month))

        response = [MonthlyPaymentResponse(
            id=daily.id,
            balance=daily.balance,
            profit=daily.profit,
            day=daily.day
        ) for daily in dailies]

        return MonthlyPaymentListResponse(payments=response)
