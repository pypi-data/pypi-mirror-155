from datetime import datetime

from easytradesdk.Serializer import DeserializableObject


class Condition(DeserializableObject):

    def __init__(self, identify: str = None, conditionData: dict = None):
        self.__identify = identify  # 开仓/卖出条件的标识
        self.__timeStamp = int(round(datetime.now().timestamp() * 1000))  # 开仓/卖出条件产生的时间
        self.__conditionData = conditionData  # 开仓/卖出条件产生时的用户数据
        self.__canceled = False

    def getObjectMapper(self):
        return {"__conditionData": dict}

    def cancel(self):
        self.__canceled = True

    def isCanceled(self):
        return self.__canceled

    def getIdentify(self):
        return self.__identify

    def generateBuyOrderSignal(self, signalData: dict = None):
        return OrderSignal(self, 1, signalData)

    def generateSellOrderSignal(self, signalData: dict = None):
        return OrderSignal(self, -1, signalData)


class OrderSignal(DeserializableObject):

    def __init__(self, condition: Condition = None, signalType: int = None, signalData: dict = None):
        self.__condition = condition
        self.__signalType = signalType  # 1 买入 -1 卖出
        self.__timeStamp = int(round(datetime.now().timestamp() * 1000))  # 买入或卖出信号产生的时间
        self.__signalData = signalData  # 买入或卖出信号产生时的信号数据
        self.__isSignalExecuted = False  # 信号是否已经执行

    def getObjectMapper(self):
        return {"__condition": Condition, "__signalData": dict}

    def isExecuted(self):
        return self.__isSignalExecuted

    def executedCallBack(self):
        self.__isSignalExecuted = True

    def getCondition(self):
        return self.__condition
