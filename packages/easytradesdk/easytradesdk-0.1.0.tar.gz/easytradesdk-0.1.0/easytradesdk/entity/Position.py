import decimal

from easytradesdk.Serializer import DeserializableObject


class Position(DeserializableObject):

    def __init__(self):
        self.tc = None
        self.symbol = None
        self.initialTicker = decimal.Decimal('0')
        self.initialAmount = decimal.Decimal('0')
        self.initialHolding = decimal.Decimal('0')
        self.initialTotalAmount = decimal.Decimal('0')
        self.remainAmount = decimal.Decimal('0')
        self.remainHolding = decimal.Decimal('0')
        self.lastDealAmount = decimal.Decimal('0')
        self.lastDealQuantity = decimal.Decimal('0')
        self.lastTicker = decimal.Decimal('0')

    def getObjectMapper(self):
        return {"initialTicker": decimal.Decimal, "initialAmount": decimal.Decimal,
                "initialHolding": decimal.Decimal, "initialTotalAmount": decimal.Decimal,
                "remainAmount": decimal.Decimal, "remainHolding": decimal.Decimal,
                "lastDealAmount": decimal.Decimal, "lastDealQuantity": decimal.Decimal, "lastTicker": decimal.Decimal}
