from enum import Enum


class TC(Enum):
    BINANCE = "BINANCE"

    @staticmethod
    def parse(tc):
        result = list(filter(lambda c: c.value == tc, TC))
        if result:
            return result[0]
        return None
