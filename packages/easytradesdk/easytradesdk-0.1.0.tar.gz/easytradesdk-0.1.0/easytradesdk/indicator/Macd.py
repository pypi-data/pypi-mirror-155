import decimal

import numpy as np
import talib._ta_lib as ta

from easytradesdk.Serializer import DeserializableObject


class Macd(DeserializableObject):

    def __init__(self, diff=None, dea=None, value=None):
        self.diff = diff
        self.dea = dea
        self.value = value

    def getObjectMapper(self):
        return {"diff": decimal.Decimal, "dea": decimal.Decimal, "value": decimal.Decimal}

    @staticmethod
    def generate(np_closing_price_array, fast_period, slow_period, signal_period):

        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _np_macd_array = ta.MACD(np_closing_price_array, fast_period, slow_period, signal_period)

        _macd_list = []

        for _index in range(0, len(np_closing_price_array)):
            _diff = _np_macd_array[0][_index]
            _dea = _np_macd_array[1][_index]
            _value = _np_macd_array[2][_index]

            if np.isnan(_diff) or np.isnan(_dea) or np.isnan(_value):
                _macd_list.append(None)
            else:
                _macd_list.append(Macd(_diff, _dea, _value))

        return _macd_list
