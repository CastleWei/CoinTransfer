from utils import Direction
from base_platform import BasePlatform
import grequests

class GateIO(BasePlatform):
    platform_name = 'GateIO'
    # url = 'api.gateio.io'

    # api_key = '00'
    # secret_key = '00'

    support_coins = ['btc', 'eth']
    infos = dict(
        btc=dict(
            key='$btc',
            交易手续费比例=0.002,
            提现手续费定额=0.001,
        ),
        eth=dict(
            key='$eth',
            交易手续费比例=0.002,
            提现手续费定额=0.003,
        )
    )
    
    @classmethod
    def _request_info(cls, coin: str, buy_or_sell: Direction):
        url = 'https://data.gateio.io/api2/1/orderBook/%s_usdt' % coin
        d = grequests.get(url).send().response.json()

        inf = cls.infos[coin]
        inf['卖盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['asks'])]
        inf['卖盘'].reverse()
        inf['买盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['bids'])]
        inf['卖1价'] = inf['卖盘'][0][0]
        inf['买1价'] = inf['买盘'][0][0]
