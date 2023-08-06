from easytradesdk.indicator.SimpleIndicator import SimpleIndicator
import talib._ta_lib as ta


class Ma(SimpleIndicator):

    def __init__(self):
        super(Ma, self).__init__()

    @staticmethod
    def generate(np_closing_price_array, time_periods):

        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _ma_dict = {}
        for _t in range(0, len(time_periods)):
            _time_period = time_periods[_t]
            _ma_dict[_time_period] = ta.MA(np_closing_price_array, timeperiod=_time_period, matype=0)

        _ma_array = []
        for _index in range(0, len(np_closing_price_array)):
            _ma = Ma()
            for t in range(0, len(time_periods)):
                _time_period = time_periods[t]
                _np_ma_array = _ma_dict[_time_period]
                _v = _np_ma_array[_index]

                if _v is not None:
                    _ma.setValue(_v, _time_period)
                else:
                    _ma.setValue(None, _time_period)
            _ma_array.append(_ma)

        return _ma_array
