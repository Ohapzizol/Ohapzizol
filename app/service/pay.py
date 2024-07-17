from datetime import date, datetime
from typing import List

from fastapi import HTTPException

from app.db.base import find_all_payments_by_user_id_and_date, find_all_payments_by_user_id_and_last_six, \
    find_all_monthly_payment_by_user_id_at_now, save_new_payment, update_user, save_daily, find_daily_by_user_id_at_now, \
    update_daily, find_pay_by_id, delete_pay
from app.db.models.user import User
from app.dto import PaymentResponse, StatisticsPaymentsResponse, WritePaymentRequest, PaymentType
from app.jwt.jwt import getCurrentUser


class PayService:

    @staticmethod
    async def getPaymentsByDate(_date: date, _user: User) -> List[PaymentResponse]:
        payments = await find_all_payments_by_user_id_and_date(_userId=_user.id, _date=_date)

        if not payments:
            raise HTTPException(204, "There is no payment for this date" + str(_date))

        return [PaymentResponse(
            id=pay.id,
            title=pay.title,
            value=pay.value,
            description=pay.description,
            tag=pay.tag,
            time=pay.time
        ) for pay in payments]

    @staticmethod
    async def getPaymentsLatestStatistics(_token: str) -> StatisticsPaymentsResponse:
        user = await getCurrentUser(_token)

        payments = await find_all_payments_by_user_id_and_last_six(user.id)

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

    @staticmethod
    async def getPaymentsTagStatistics(_token: str) -> StatisticsPaymentsResponse:
        user = await getCurrentUser(_token)

        payments = await find_all_monthly_payment_by_user_id_at_now(user.id)

        if not payments:
            raise HTTPException(204, "There is no content")

        response = dict()

        for pay in payments:
            if pay.tag in response:
                if pay.value < 0:
                    response[pay.tag]['expenditure'] -= pay.value
                else:
                    response[pay.tag]['income'] += pay.value
            else:
                if pay.value < 0:
                    response[pay.tag] = {'expenditure': -pay.value, 'income': 0}
                else:
                    response[pay.tag] = {'expenditure': 0, 'income': pay.value}

        return StatisticsPaymentsResponse(statistics=response)

    @staticmethod
    async def createPayment(request: WritePaymentRequest, _token: str) -> None:
        user = await getCurrentUser(_token)

        value = request.value if request.typ == PaymentType.income else -request.value

        await save_new_payment(
            request.title,
            value,
            request.description,
            date.today(),
            request.time,
            request.tag,
            user.id,
        )

        balance = user.balance + value

        await update_user(user.id, user.name, user.password, balance)

        daily = await find_daily_by_user_id_at_now(user.id)

        if daily:
            await update_daily(_id=daily.id, _profit=daily.profit + value, _balance=balance, _user_id=user.id)
        else:
            await save_daily(_profit=value, _balance=balance, _user_id=user.id)

    @staticmethod
    async def deleteById(_pay_id: int, _token: str):
        user = await getCurrentUser(_token)
        payment = await find_pay_by_id(_pay_id)

        if not payment:
            raise HTTPException(404, 'Payment not found')

        if user.id != payment.user_id:
            raise HTTPException(403, "permission denied")

        if payment.date != datetime.now().date():
            raise HTTPException(400, "you can't delete this payment")

        await delete_pay(payment)









