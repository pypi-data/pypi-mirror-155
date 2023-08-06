from easytradesdk.indicator.SimpleIndicator import SimpleIndicator
import talib._ta_lib as ta


class Ema(SimpleIndicator):

    def __init__(self):
        super(Ema, self).__init__()

    @staticmethod
    def generate(np_closing_price_array, time_periods):

        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _ema_dict = {}
        for _t in range(0, len(time_periods)):
            _time_period = time_periods[_t]
            _ema_dict[_time_period] = ta.EMA(np_closing_price_array, timeperiod=_time_period)

        _ema_array = []
        for _index in range(0, len(np_closing_price_array)):
            _ema = Ema()
            for t in range(0, len(time_periods)):
                _time_period = time_periods[t]
                _np_ema_array = _ema_dict[_time_period]
                _v = _np_ema_array[_index]

                if _v is not None:
                    _ema.setValue(_v, _time_period)
                else:
                    _ema.setValue(None, _time_period)
            _ema_array.append(_ema)

        return _ema_array
