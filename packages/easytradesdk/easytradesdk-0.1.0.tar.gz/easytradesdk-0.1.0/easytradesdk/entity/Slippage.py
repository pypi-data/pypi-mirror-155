'''
    模拟交易或者回测时需要设置的滑点
'''
import decimal

from easytradesdk.Serializer import DeserializableObject


class Slippage(DeserializableObject):

    def __init__(self, slippageType=1, value=decimal.Decimal('0')):
        # 滑点类型 1:百分比  2:某个具体的值
        self.slippageType = slippageType

        self.value = value

    def getObjectMapper(self):
        return {"value": decimal.Decimal}
