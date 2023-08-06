import datetime
import decimal

from easytradesdk.Serializer import DeserializableObject


class Kline(DeserializableObject):

    def __init__(self):
        self.tc = None
        self.symbol = None
        self.timeInterval = None
        self.timeMills = None
        self.endTimeMills = None
        self.startTime = None
        self.endTime = None
        self.openingPrice = None
        self.closingPrice = None
        self.highPrice = None
        self.lowPrice = None
        self.volume = None
        self.quantity = None
        self.cnt = None
        self.buyVolume = None
        self.buyQuantity = None

    def getObjectMapper(self):
        return {
            "startTime": datetime.datetime, "endTime": datetime.datetime,
            "openingPrice": decimal.Decimal, "closingPrice": decimal.Decimal,
            "highPrice": decimal.Decimal, "lowPrice": decimal.Decimal,
            "volume": decimal.Decimal, "quantity": decimal.Decimal,
            "buyVolume": decimal.Decimal, "buyQuantity": decimal.Decimal}

    def isFall(self):
        return self.closingPrice < self.openingPrice

    def isRise(self):
        return self.closingPrice > self.openingPrice

    @staticmethod
    def getCount(startTimeMills, endTimeMills, interval):

        symbol = interval[-1]
        cnt = int(interval[0:len(interval) - 1])

        if symbol == 'm':
            return int((startTimeMills - endTimeMills) / (cnt * 60 * 1000))

        if symbol == 'h':
            return int((startTimeMills - endTimeMills) / (cnt * 3600 * 1000))

        if symbol == 'd':
            return int((startTimeMills - endTimeMills) / (cnt * 3600 * 24 * 1000))

        return 0
