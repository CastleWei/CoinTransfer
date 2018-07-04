from pprint import pprint
import sys
sys.path.append(r"C:\Users\VinceWay\PycharmProjects\CoinTransfer")
from utils import TransferScheme

platfroms = []

from coin_platforms.GateIO import GateIO
platfroms.append(GateIO)
from coin_platforms.DragonEx import DragonEx
platfroms.append(DragonEx)
from coin_platforms.Huobi import Huobi
platfroms.append(Huobi)

schemes = [
    # TransferScheme(GateIO, 'btc', DragonEx),
    # TransferScheme(DragonEx, 'btc', GateIO),
    # TransferScheme(GateIO, 'eth', DragonEx),
    # TransferScheme(DragonEx, 'eth', GateIO),
    # TransferScheme(GateIO, 'btc', Huobi),
    # TransferScheme(GateIO, 'eth', Huobi),
    # TransferScheme(Huobi, 'eth', DragonEx),
]

pprint(schemes)

for src in platfroms:
    for dst in platfroms:
        if src is dst:
            continue
        for coin in src.infos:
            if coin in dst.infos:
                schemes.append(TransferScheme(src, coin, dst))

pprint(schemes)
for s in schemes:
    print(s.repr)
