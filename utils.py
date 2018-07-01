from enum import Enum, auto

class Direction(Enum):
    Buy = auto()
    Sell = auto()

class TransferScheme:

    def __init__(self, src, coin, dst):
        self.src = src
        self.coin = coin
        self.dst = dst

    # def profit(self):
    #     pass