from fastapi import HTTPException

from app.db.base import find_all_daily_by_user_id_and_year_and_month, find_daily_by_user_id_at_now
from app.db.models.user import User
from app.dto import MonthlyResponse, DailyResponse
from app.jwt.jwt import getCurrentUser


class DailyService:

    @staticmethod
    async def getMonthlyDaily(_year: int, _month: int, _token: str) -> MonthlyResponse:
        user = await getCurrentUser(_token)

        dailies = await find_all_daily_by_user_id_and_year_and_month(user.id, _year, _month)

        if not dailies:
            raise HTTPException(204, "There is no content by date: " + str(_year) + '.' + str(_month))

        response = [DailyResponse(
            id=daily.id,
            balance=daily.balance,
            profit=daily.profit,
            day=daily.day
        ) for daily in dailies]

        return MonthlyResponse(payments=response)

    @staticmethod
    async def getDaily(_user: User) -> (int, int):
        daily = await find_daily_by_user_id_at_now(_userId=_user.id)
        return daily.profit, daily.balance

