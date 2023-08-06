from enum import Enum


class Symbol(Enum):
    BTC_USDT = "BTC_USDT"
    ETH_BTC = "ETH_BTC"
    ETH_USDT = "ETH_USDT"

    @staticmethod
    def parse(symbol):
        result = list(filter(lambda c: c.value == symbol, Symbol))
        if result:
            return result[0]
        return None
