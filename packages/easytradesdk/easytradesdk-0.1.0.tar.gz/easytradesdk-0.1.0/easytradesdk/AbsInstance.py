import abc


class AbsInstance(metaclass=abc.ABCMeta):

    # 实例初始化
    @abc.abstractmethod
    def init(self):
        pass

    # 实例销毁
    @abc.abstractmethod
    def destroy(self):
        pass

    # 实例执行函数，子类需要重写
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def executeStopLoss(self):
        pass

    @abc.abstractmethod
    def executeStopProfit(self):
        pass
