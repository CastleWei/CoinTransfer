from utils import Direction
from base_platform import BasePlatform
import grequests

class Huobi(BasePlatform):
    platform_name = 'Huobi'
    # url = 'api.huobi.br.com'

    # api_key = '00'
    # secret_key = '00'

    support_coins = ['btc', 'eth']
    infos = dict(
        btc=dict(
            key='$btc',
            交易手续费比例=0.002,
            提现手续费定额=0.004,
        ),
        eth=dict(
            key='$eth',
            交易手续费比例=0.002,
            提现手续费定额=0.01,
        )
    )
    
    @classmethod
    def _request_info(cls, coin: str, buy_or_sell: Direction):
        url = 'https://api.huobi.br.com/market/depth?symbol=%susdt&type=step1' % coin
        d = grequests.get(url).send().response.json()['tick']

        inf = cls.infos[coin]
        inf['卖盘'] = d['asks']
        inf['买盘'] = d['bids']
        inf['卖1价'] = inf['卖盘'][0][0]
        inf['买1价'] = inf['买盘'][0][0]
