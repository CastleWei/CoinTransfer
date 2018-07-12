from coin_platforms.base_platform import BasePlatform
import grequests
from collections import defaultdict

class GateIO(BasePlatform):
    platform_name = 'GateIO'
    # url = 'api.gateio.io'

    # api_key = '00'
    # secret_key = '00'

    usdt = dict(
        price_to_buy=0,
        price_to_sell=0
    )
    to_notify = defaultdict(list)

    coin_infos = dict(
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
    def _request_info(cls, coin: str):
        url = 'https://data.gateio.io/api2/1/orderBook/%s_usdt' % coin
        r = grequests.get(url).send().response
        if not r: raise ValueError

        d = r.json()
        inf = cls.coin_infos[coin]
        inf['卖盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['asks'])]
        inf['卖盘'].reverse()
        inf['买盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['bids'])]
        inf['卖1价'] = inf['卖盘'][0][0]
        inf['买1价'] = inf['买盘'][0][0]

    @classmethod
    def _request_usdt(cls):
        url = 'https://data.gateio.io/api2/1/ticker/usdt_cny'
        r = grequests.get(url).send().response
        if not r: raise ValueError
        d = r.json()
        cls.usdt['price_to_buy'] = float(d['highestBid'])
        cls.usdt['price_to_sell'] = float(d['lowestAsk'])
