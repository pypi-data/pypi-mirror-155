import decimal

import numpy as np
import talib._ta_lib as ta

from easytradesdk.Serializer import DeserializableObject


class Boll(DeserializableObject):

    def __init__(self, upper=None, middle=None, down=None):
        self.upper = upper
        self.middle = middle
        self.down = down

    def getObjectMapper(self):
        return {"upper": decimal.Decimal, "middle": decimal.Decimal, "down": decimal.Decimal}

    @staticmethod
    def generate(np_closing_price_array, time_period, nbdevup, nbdevdn, ma_type):

        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _np_boll_Array = ta.BBANDS(np_closing_price_array, time_period, nbdevup, nbdevdn, ma_type)

        _boll_array = []

        for index in range(0, len(np_closing_price_array)):
            _boll_upper = _np_boll_Array[0][index]
            _boll_middle = _np_boll_Array[1][index]
            _boll_down = _np_boll_Array[2][index]

            if np.isnan(_boll_upper) or np.isnan(_boll_middle) or np.isnan(_boll_down):
                _boll_array.append(None)
            else:
                _boll_array.append(Boll(_boll_upper, _boll_middle, _boll_down))

        return _boll_array

    @staticmethod
    def getBollMiddles(_boll_array):
        _result = []
        for i in range(0, len(_boll_array)):
            _result.append(_boll_array[i].middle)
        return _result

    @staticmethod
    def getBollUppers(_boll_array):
        _result = []
        for i in range(0, len(_boll_array)):
            _result.append(_boll_array[i].upper)
        return _result

    @staticmethod
    def getBollDowns(_boll_array):
        _result = []
        for i in range(0, len(_boll_array)):
            _result.append(_boll_array[i].down)
        return _result
