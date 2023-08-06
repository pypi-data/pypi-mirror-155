from easytradesdk.Serializer import DeserializableObject


class SimpleIndicator(DeserializableObject):

    def __init__(self):
        self.value = None

    def getObjectMapper(self):
        return {"value": dict}

    def setValue(self, value, time_period):
        if self.value is None:
            self.value = {time_period: value}
        else:
            self.value[time_period] = value

    def getValue(self, time_period):
        return self.value[time_period]

    def getWholeValue(self):
        return self.value
