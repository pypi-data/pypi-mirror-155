import abc

from easytradesdk.entity.KlineInterval import KlineInterval
from easytradesdk.entity.Symbol import Symbol
from easytradesdk.entity.TC import TC


class AbsMarketApi(metaclass=abc.ABCMeta):

    def fetchKline(self, tc: TC, symbol: Symbol, interval: KlineInterval, startTimeMills=None, endTimeMills=None, limit=200):
        pass

    def fetchLatestKline(self, tc: TC, symbol: Symbol, interval: KlineInterval, endTimeMills=None, limit=200, excludeCurrent=None):
        pass

    def fetchDepth(self, tc: TC, symbol: Symbol, depthLimit=100):
        pass

    def fetchTicker(self, tc: TC, symbol: Symbol):
        pass
