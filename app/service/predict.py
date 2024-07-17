from datetime import datetime, timedelta
from http.client import HTTPException

import numpy as np
from tensorflow import keras

from app.db.base import find_all_daily_by_user_id_and_year_and_month
from app.db.models.user import User
from app.jwt.jwt import getCurrentUser


async def getTotalProfitByMonth(_user: User, _year: int, _month: int):
    dailies = await find_all_daily_by_user_id_and_year_and_month(_user.id, _year, _month)

    if not dailies:
        raise HTTPException(204, "There is no content by date: " + str(_year) + '.' + str(_month))

    return sum([daily.profit for daily in dailies])


class PredictService:

    @staticmethod
    async def getPredictComment(_user: User):
        model = keras.models.load_model('app/service/model/model.keras')
        one_month_ago = (datetime.now() - timedelta(days=1))
        money = await getTotalProfitByMonth(_user, one_month_ago.year, one_month_ago.month)
        pred = model.predict(np.array([money]))[0][0]
        model.compile(loss='mse', optimizer='rmsprop')
        model.fit(np.array([money]), np.array([pred]), batch_size=1, epochs=50, verbose=1)
        model.save('app/service/model/model1.keras')
        return f'다음 달의 예상 지출액은 {pred // 10 * 10:.0f}원 입니다.'