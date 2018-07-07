from coin_platforms.base_platform import BasePlatform
import grequests

class DragonEx(BasePlatform):
    platform_name = 'DragonEx'
    # url = 'openapi.dragonex.im'

    # api_key = '00'
    # secret_key = '00'

    coin_infos = dict(
        btc=dict(
            key='$btc',
            symbol_id='101',
            交易手续费比例=0.002,
            提现手续费定额=0.001,
        ),
        eth=dict(
            key='$eth',
            symbol_id='103',
            交易手续费比例=0.002,
            提现手续费定额=0.01,
        )
    )
    
    @classmethod
    def _request_info(cls, coin: str):
        inf = cls.coin_infos[coin]
        r = grequests.map((
                grequests.get('https://openapi.dragonex.im/api/v1/market/sell/?symbol_id=' + inf['symbol_id']),
                grequests.get('https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=' + inf['symbol_id'])
        ))
        if not r[0] or not r[1]: raise ValueError

        inf['卖盘'] = [i for i in map(lambda x: (float(x['price']), float(x['volume'])), r[0].json()['data'])]
        inf['买盘'] = [i for i in map(lambda x: (float(x['price']), float(x['volume'])), r[1].json()['data'])]
        inf['卖1价'] = inf['卖盘'][0][0]
        inf['买1价'] = inf['买盘'][0][0]
