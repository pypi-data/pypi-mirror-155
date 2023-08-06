from easytradesdk.indicator.SimpleIndicator import SimpleIndicator
import talib._ta_lib as ta


class Wma(SimpleIndicator):

    def __init__(self):
        super(Wma, self).__init__()

    @staticmethod
    def generate(np_closing_price_array, time_periods):

        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _wma_dict = {}
        for _t in range(0, len(time_periods)):
            _time_period = time_periods[_t]
            _wma_dict[_time_period] = ta.WMA(np_closing_price_array, timeperiod=_time_period)

        _wma_array = []
        for _index in range(0, len(np_closing_price_array)):
            _wma = Wma()
            for t in range(0, len(time_periods)):
                _time_period = time_periods[t]
                _np_wma_array = _wma_dict[_time_period]
                _v = _np_wma_array[_index]

                if _v is not None:
                    _wma.setValue(_v, _time_period)
                else:
                    _wma.setValue(None, _time_period)
            _wma_array.append(_wma)

        return _wma_array
