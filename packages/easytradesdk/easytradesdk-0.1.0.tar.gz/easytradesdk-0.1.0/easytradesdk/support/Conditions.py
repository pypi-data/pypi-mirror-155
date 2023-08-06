from easytradesdk.Serializer import DeserializableObject
from easytradesdk.support.Condition import Condition


class Conditions(DeserializableObject):
    __DEFAULT_IDENTIFY = "default"

    def __init__(self):
        self.__conditions = []

    def getObjectMapper(self):
        return {"__conditions", list}

    def exists(self, identify: str = __DEFAULT_IDENTIFY):
        return self.get(identify) is not None

    def get(self, identify: str = __DEFAULT_IDENTIFY):
        if self.__conditions:
            for _condition in self.__conditions:
                if _condition.getIdentify() == identify:
                    return _condition
        return None

    def clear(self):
        for _condition in self.__conditions:
            if _condition is not None:
                _condition.cancel()
        self.__conditions.clear()

    def remove(self, identify: str = __DEFAULT_IDENTIFY):
        _idxs = []
        for _index, _condition in enumerate(self.__conditions):
            if _condition.getIdentify() == identify:
                _idxs.append(_index)

        for _i in _idxs:
            del self.__conditions[_i]

    def cancel(self, identify: str = __DEFAULT_IDENTIFY):
        _condition = self.get(identify)
        if _condition:
            _condition.cancel()

    def cancelAll(self):
        for _condition in self.__conditions:
            _condition.cancel()

    def generate(self, conditionData: dict = None, identify: str = __DEFAULT_IDENTIFY):
        _condition = Condition(identify, conditionData)
        self.__conditions.append(_condition)
        return _condition
