from enum import Enum, auto

class Direction(Enum):
    Buy = auto()
    Sell = auto()

class TransferScheme:

    def __init__(self, src, coin, dst):
        self.src = src
        self.coin = coin
        self.dst = dst

        self.name = '%s$$%s$$%s' % (src.platform_name, coin, dst.platform_name)  # eg. 'GateIO$$eth$$DragonEx'
        self.repr = '%s --> %s --> %s' % (src.platform_name, coin, dst.platform_name)  # eg. 'GateIO --> eth --> DragonEx'

    # def profit(self):
    #     pass