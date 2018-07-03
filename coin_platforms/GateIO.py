import time
from utils import Direction
import grequests

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

timeliness = 5
req_timeout = 5


def prepare_info(coin: str, buy_or_sell: Direction):
    inf = {}
    if coin in infos:
        inf = infos[coin]
        inf.setdefault('update_time', 0)
        # TODO: 手续费也实时从网站请求
    else:
        # 暂不支持其他币
        print('coin %s is not supported!' % coin)
        return False

    if time.time() - inf['update_time'] > timeliness:
        # 发起请求获取数据
        url = 'https://data.gateio.io/api2/1/orderBook/%s_usdt' % coin
        d = grequests.get(url).send().response.json()
        inf['update_time'] = time.time()
        inf['卖盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['asks'])]
        inf['卖盘'].reverse()
        inf['买盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['bids'])]
        inf['卖1价'] = inf['卖盘'][0][0]
        inf['买1价'] = inf['买盘'][0][0]
    
    # 检查需要的数据是否已获取且格式正确
    try:
        assert inf['卖盘'][0][0] > 0 and inf['卖盘'][0][1] > 0
        assert inf['买盘'][0][0] > 0 and inf['买盘'][0][1] > 0
        assert inf['卖盘'][0][0] < inf['卖盘'][1][0]
        assert inf['买盘'][0][0] > inf['买盘'][1][0]
        assert inf['卖1价'] > 0
        assert inf['买1价'] > 0
        assert inf['卖1价'] > inf['买1价']
    except (KeyError, TypeError, AssertionError) as e:
        print('prepare info wrong...', e.__class__.__name__, e)
        return False
    else:
        # 返回成功
        return True


def can_buy(coin: str, total_money):
    inf = infos[coin]
    # TODO: 测试
    return total_money / inf['卖1价'] * (1 - inf['交易手续费比例']) - inf['提现手续费定额']


def can_sell(coin: str, amount):
    need_money = 0
    买盘 = infos[coin]['买盘']
    for price, volumn in 买盘:
        if volumn < amount:
            # 这一笔卖不完
            need_money += price * volumn
            amount -= volumn
        else:
            need_money += price * amount
            amount = 0
            break
    # TODO: 测试
    return need_money
