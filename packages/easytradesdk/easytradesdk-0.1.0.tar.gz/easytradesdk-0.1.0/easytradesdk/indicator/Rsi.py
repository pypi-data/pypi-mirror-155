from easytradesdk.indicator.SimpleIndicator import SimpleIndicator
import talib._ta_lib as ta


class Rsi(SimpleIndicator):

    def __init__(self):
        super(Rsi, self).__init__()

    @staticmethod
    def generate(np_closing_price_array, time_periods):
        if np_closing_price_array is None or len(np_closing_price_array) == 0:
            return []

        _rsi_tmp_dict = {}
        for t in range(0, len(time_periods)):
            _time_period = time_periods[t]

            _rsi_tmp_dict[_time_period] = ta.RSI(np_closing_price_array, timeperiod=_time_period)

        _rsi_array = []
        for _index in range(0, len(np_closing_price_array)):

            _rsi = Rsi()
            for _t in range(0, len(time_periods)):
                _time_period = time_periods[_t]
                _np_rsi_array = _rsi_tmp_dict[_time_period]
                _rsi_value = _np_rsi_array[_index]

                if _rsi_value is not None:
                    _rsi.setValue(_rsi_value, _time_period)
                else:
                    _rsi.setValue(None, _time_period)
            _rsi_array.append(_rsi)

        return _rsi_array
