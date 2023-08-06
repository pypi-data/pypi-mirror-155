import numpy as np


class KlineSupporter:

    def __init__(self, klines):

        self.__openingPriceList = []
        self.__closingPriceList = []
        self.__highPriceList = []
        self.__lowPriceList = []
        self.__openingPriceNpArray = None
        self.__closingPriceNpArray = None
        self.__highPriceNpArray = None
        self.__lowPriceNpArray = None

        if klines is not None and len(klines) > 0:

            for idx in range(0, len(klines)):
                self.__openingPriceList.append(klines[idx].openingPrice)
                self.__closingPriceList.append(klines[idx].closingPrice)
                self.__highPriceList.append(klines[idx].highPrice)
                self.__lowPriceList.append(klines[idx].lowPrice)

            self.__openingPriceNpArray = np.array(self.__openingPriceList, dtype=np.double)
            self.__closingPriceNpArray = np.array(self.__closingPriceList, dtype=np.double)
            self.__highPriceNpArray = np.array(self.__highPriceList, dtype=np.double)
            self.__lowPriceNpArray = np.array(self.__lowPriceList, dtype=np.double)

    def getOpeningPriceList(self):
        return self.__openingPriceList

    def getClosingPriceList(self):
        return self.__closingPriceList

    def getHighPriceList(self):
        return self.__highPriceList

    def getLowPriceList(self):
        return self.__lowPriceList

    def getOpeningPriceNpArray(self):
        return self.__openingPriceNpArray

    def getClosingPriceNpArray(self):
        return self.__closingPriceNpArray

    def getHighPriceNpArray(self):
        return self.__highPriceNpArray

    def getLowPriceNpArray(self):
        return self.__lowPriceNpArray

    def clear(self):
        self.__closingPriceList = []
        self.__highPriceList = []
        self.__lowPriceList = []
        self.__closingPriceNpArray = None
        self.__highPriceNpArray = None
        self.__lowPriceNpArray = None
