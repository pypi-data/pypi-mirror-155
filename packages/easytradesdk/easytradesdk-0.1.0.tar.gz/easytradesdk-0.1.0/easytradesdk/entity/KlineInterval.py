from enum import Enum


class KlineInterval(Enum):
    S_1m = "1m"
    S_3m = "3m"
    S_5m = "5m"
    S_15m = "15m"
    S_30m = "30m"
    S_1h = "1h"
    S_2h = "2h"
    S_4h = "4h"
    S_6h = "6h"
    S_8h = "8h"
    S_12h = "12h"
    S_1d = "1d"
    S_3d = "3d"
    S_1W = "1w"
    S_1M = "1M"

    @staticmethod
    def parse(interval):
        result = list(filter(lambda c: c.value == interval, KlineInterval))
        if result:
            return result[0]
        return None
