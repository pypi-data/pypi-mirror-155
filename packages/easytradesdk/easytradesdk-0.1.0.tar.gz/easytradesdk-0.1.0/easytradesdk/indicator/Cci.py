from easytradesdk.indicator.SimpleIndicator import SimpleIndicator
import talib._ta_lib as ta


class Cci(SimpleIndicator):

    def __init__(self):
        super(Cci, self).__init__()

    @staticmethod
    def generate(np_high_price_array, np_low_price_array, np_closing_price_array, time_periods):

        if (np_high_price_array is None or len(np_high_price_array) == 0) or \
                (np_low_price_array is None or len(np_low_price_array) == 0) or \
                (np_closing_price_array is None or len(np_closing_price_array) == 0):
            return []

        _cci_tmp_dict = {}
        for _t in range(0, len(time_periods)):
            _time_period = time_periods[_t]
            _cci_tmp_dict[_time_period] = ta.CCI(np_high_price_array, np_low_price_array, np_closing_price_array, timeperiod=_time_period)
        _cci_array = []
        for _index in range(0, len(np_closing_price_array)):

            _cci = Cci()

            for t in range(0, len(time_periods)):
                _time_period = time_periods[t]
                _np_cci_Array = _cci_tmp_dict[_time_period]
                _cci_value = _np_cci_Array[_index]

                if _cci_value is not None:
                    _cci.setValue(_cci_value, _time_period)
                else:
                    _cci.setValue(None, _time_period)
            _cci_array.append(_cci)

        return _cci_array
