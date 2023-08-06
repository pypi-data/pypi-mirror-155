import abc


class AbsContext(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getPosition(self, tc, symbol):
        pass

    @abc.abstractmethod
    def getPositions(self):
        pass

    @abc.abstractmethod
    def getStrategyParams(self):
        pass

    @abc.abstractmethod
    def getExecuteInterval(self):
        pass

    @abc.abstractmethod
    def getExecutingTimeMills(self):
        pass

    @abc.abstractmethod
    def getMarketApi(self):
        pass

    @abc.abstractmethod
    def getTradeApi(self):
        pass
