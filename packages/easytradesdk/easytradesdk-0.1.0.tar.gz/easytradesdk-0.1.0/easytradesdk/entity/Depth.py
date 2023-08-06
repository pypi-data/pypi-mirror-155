import decimal

from easytradesdk.Serializer import DeserializableObject


class DepthValue(DeserializableObject):

    def __init__(self):
        self.price = None
        self.quantity = None

    def getObjectMapper(self):
        return {"price": decimal.Decimal, "quantity": decimal.Decimal}


class Depth(DeserializableObject):

    def __init__(self):
        self.bids = []
        self.asks = []

    def getObjectMapper(self):
        return {"bids": DepthValue, "asks": DepthValue}
