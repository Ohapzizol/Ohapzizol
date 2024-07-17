from datetime import datetime, timedelta
from math import floor

import numpy as np
from fastapi import HTTPException
from tensorflow import keras

from app.db.base import find_all_daily_by_user_id_and_year_and_month
from app.db.models.user import User


class PredictService:

    @staticmethod
    async def getPredictComment(_user: User):
        model = keras.models.load_model('app/service/model/model.keras')
        one_month_ago = (datetime.now() - timedelta(days=1))

        dailies = await find_all_daily_by_user_id_and_year_and_month(_user.id, one_month_ago.year, one_month_ago.month)

        if not dailies:
            raise HTTPException(204, "There is no content by date")

        money = sum([daily.profit for daily in dailies])

        pred = model.predict(np.array([money]))[0][0]
        model.compile(loss='mse', optimizer='rmsprop')
        model.fit(np.array([money]), np.array([pred]), batch_size=1, epochs=50, verbose=1)
        model.save('app/service/model/model1.keras')

        return f'다음 달의 예상 총수익은 {format(floor(pred // 10 * 10), ",")}원 입니다.'
