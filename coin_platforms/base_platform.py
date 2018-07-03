from abc import ABC, abstractmethod
import time
from utils import Direction


class BasePlatform(ABC):
    platform_name = 'undefined'
    support_coins = []
    infos = {}
    
    timeliness = 5
    req_timeout = 5

    @classmethod
    @abstractmethod
    def _request_info(cls, coin: str, buy_or_sell: Direction):
        pass

    @classmethod
    def prepare_info(cls, coin: str, buy_or_sell: Direction):
        inf = {}
        if coin in cls.infos:
            inf = cls.infos[coin]
            inf.setdefault('update_time', 0)
            # TODO: 手续费也实时从网站请求
        else:
            # 暂不支持其他币
            print('coin %s is not supported!' % coin)
            return False

        if time.time() - inf['update_time'] > cls.timeliness:
            # 发起请求获取数据
            cls._request_info(coin, buy_or_sell)
            inf['update_time'] = time.time()

            ## 以下为 cls._request_info() 的示例
            # url = 'https://data.gateio.io/api2/1/orderBook/%s_usdt' % coin
            # d = grequests.get(url).send().response.json()
            # inf['卖盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['asks'])]
            # inf['卖盘'].reverse()
            # inf['买盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['bids'])]
            # inf['卖1价'] = inf['卖盘'][0][0]
            # inf['买1价'] = inf['买盘'][0][0]
        
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


    @classmethod
    def can_buy(cls, coin: str, total_money):
        inf = cls.infos[coin]
        # TODO: 测试
        return total_money / inf['卖1价'] * (1 - inf['交易手续费比例']) - inf['提现手续费定额']


    @classmethod
    def can_sell(cls, coin: str, amount):
        need_money = 0
        买盘 = cls.infos[coin]['买盘']
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

